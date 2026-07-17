from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from typing import Callable, Literal, Union, overload, Protocol
from threading import Timer
import git

type event = Literal["created","modified","deleted","moved"]
type git_event = Literal["commit","branch"]

exclusion_list = [".lock"]
ref_path = ".git/refs/heads/"
main_path = ".git/"

class ExtFuncProtocol(Protocol):
    @overload
    def __call__(self, action: Literal["commit"]) -> None: ...
    @overload
    def __call__(self, action: Literal["branch"], branch_name: str | None) -> None: ...
    def __call__(self, action: str, branch_name: str | None = None) -> None: ...

class EventHandler(FileSystemEventHandler):
	def __init__(self,func: Callable[[git_event], None]) -> None:
		super().__init__()
		self.func = func
		self.exclusion_list = exclusion_list.copy()

	def on_created(self,evt):
		self.on_change("created",evt.src_path)

	def on_modified(self,evt):
		self.on_change("modified",evt.src_path)

	def on_deleted(self,evt):
		self.on_change("deleted",evt.src_path)

	def on_moved(self,evt):
		self.on_change("moved",evt.src_path)

	def on_change(self, type:event, path: str ):
		if self.is_excluded(path):
			return
		print("Detecting",type,path)
		if "refs" in path:
			self.func("commit")
		elif "HEAD" in path:
			self.func("branch")


	def is_excluded(self, target_path: str):
		path = Path(target_path)
		for excluded in self.exclusion_list:
			if excluded in path.parts:
				return True
			if excluded in path.suffixes:
				return True
		return False

class GitWatcher:

	def __init__(self, location: str, on_change: ExtFuncProtocol):
		git_folder = Path(location) / main_path
		commit_folder = Path(location) / ref_path
		self.location = location
		print("Git watching",git_folder,commit_folder)
		self.handler = EventHandler(self.on_event)
		self.observer = Observer()
		self.observer.schedule(self.handler, commit_folder, recursive=True)
		self.observer.schedule(self.handler, git_folder, recursive=False)
		self.timer = None
		self.on_change = on_change
		self.observer.start()

	def on_event(self,event: git_event):
		if self.timer is not None:
			self.timer.cancel()
		self.timer = Timer(1, self.ready, [event])
		self.timer.start()

	def ready(self, evt: git_event):
		if evt == "commit":
			self.on_change("commit")	
		else:
			try:
				repo = git.Repo(self.location)
				name = repo.active_branch.name
			except (git.InvalidGitRepositoryError, TypeError, ValueError):
				name = None
			print("Change happening",evt,name)
			self.on_change(evt,name)
		self.timer = None

	def stop(self):
		self.observer.stop()
		self.observer.join()
		if self.timer is not None:
			self.timer.cancel()
