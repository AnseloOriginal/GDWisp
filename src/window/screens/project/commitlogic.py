from typing import Callable

from src.window.screens.shared.forced_popup import ForcedPopup
import src.operations.git.tools as git_tools 
import threading
import queue

class CommitLogic:
	
	def __init__(self,app, msg: str, folder: str, onsuccess: Callable):
		self.popup = ForcedPopup(app)
		self.popup.title("Starting Commit")
		self.stage = "starting"
		self.msg = msg
		self.folder = folder
		self.stageQueue = queue.Queue()
		self.commitQueue = queue.Queue()

		self.stage_thread = threading.Thread(target=self.staging)
		self.commit_thread = threading.Thread(target=self.commiting)

		self._previous_excepthook = threading.excepthook
		threading.excepthook = self.handle_error
		self.onsuccess = onsuccess
		self.step()


	def staging(self):
		self.stage = "staging"
		result = git_tools.stage_all_files(self.folder)
		self.stageQueue.put(result)
		self.popup.after(0, self.step)

	def commiting(self):
		self.stage = "commiting"
		result = git_tools.commit(self.folder, self.msg)
		self.commitQueue.put(result)
		self.popup.after(0, self.step)

	def step(self):

		if self.stage == "starting":

			self.popup.add_text("Starting commit. Please wait...",False)
			self.stage_thread.start()

		elif self.stage == "staging":

			result = self.stageQueue.get(block=False)
			if result['file_count'] == 0:
				return self.end_commit(False,"cannot commit with no changes")
			self.popup.add_text(f"Staged {result['file_count']} file(s) for commit")
			self.commit_thread.start()

		elif self.stage == "commiting":

			result = self.commitQueue.get(block=False)
			self.popup.add_text(f"Commit successful ({result['hexsha'][0:6]})",True,"success")
			self.end_commit(True,"",result['hexsha'])

	def end_commit(self,was_success: bool, error: str, hexsha: str = ""):
		if was_success:
			self.onsuccess(hexsha)
		else:
			self.popup.add_text(
				f"Commit failed during {self.stage} stage",True,"error"
			)
			self.popup.add_text(f"Reason for failure is {str(error)}",True,"error")
		self.popup.show_close(True)
		
		threading.excepthook = self._previous_excepthook

	def handle_error(self,args):
		fail_str = f"Error message: {args.exc_value}"
		self._previous_excepthook(args)
		self.end_commit(False,fail_str)