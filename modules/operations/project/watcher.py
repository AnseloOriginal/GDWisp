from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from typing import Callable, Literal
from threading import Timer

type event = Literal["created","modified","deleted","moved"]
exclusion_list = [".git",".autosave"]

class ProjectEventHandler(FileSystemEventHandler):
	def __init__(self,func: Callable[[event], None]) -> None:
		super().__init__()
		self.func = func
		# In case later we want to add some extra exclusions
		self.exclusion_list = exclusion_list.copy()

	def on_created(self,evt):
		if self.is_excluded(evt.src_path):
			return
		self.func("created")

	def on_modified(self,evt):
		if self.is_excluded(evt.src_path):
			return
		self.func("modified")

	def on_deleted(self,evt):
		if self.is_excluded(evt.src_path):
			return
		self.func("deleted")

	def on_moved(self,evt):
		if self.is_excluded(evt.src_path):
			return
		self.func("moved")

	def is_excluded(self, target_path: str):
		path = Path(target_path)
		for excluded in self.exclusion_list:
			if excluded in path.parts:
				return True
		return False

class Projectwatcher:

	def __init__(self, location: str, on_change: Callable):
		self.handler = ProjectEventHandler(self.on_event)
		self.observer = Observer()
		self.observer.schedule(self.handler, location, recursive=True)
		self.timer = None
		self.on_change = on_change
		self.observer.start()

	def on_event(self,etype: event):
		if self.timer is not None:
			self.timer.cancel()
		self.timer = Timer(1, self.ready)
		self.timer.start()

	def ready(self):
		self.on_change()
		self.timer = None

	def stop(self):
		self.observer.stop()
		self.observer.join()
		if self.timer is not None:
			self.timer.cancel()
