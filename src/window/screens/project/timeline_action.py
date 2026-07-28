from threading import Thread

import customtkinter as CTk
from typing import Callable, TypedDict, Literal, Union

from src.operations.git.types import GitError
from src.window.screens.shared.error_popup import ErrorPopup
from src.window.screens.shared.confirmation import ConfirmationDialog
from src.window.screens.shared.forced_popup import ForcedPopup
from src.operations.git.commits import revert, reset, end_revert
type action = Literal["reset","revert"]
type CTkLike = Union[CTk.CTkBaseClass, CTk.CTkToplevel]

def destroyTogether(widget: CTkLike, parent: CTkLike):
	widget.bind("<Destroy>",
		lambda evt: parent.destroy() if evt.widget == widget else None
	)

class SelectedCommit(TypedDict):
	summary: str | None
	hexsha: str | None

class TimelineAction(CTk.CTkToplevel):
	def __init__(self, folder: str, parent, action: action, info: SelectedCommit, onsuccess: Callable | None = None):
		super().__init__(parent)
		self.folder = folder
		self.action = action
		self.withdraw()
		self.grab_set()
		self.onsuccess = onsuccess
		if (info["summary"] and info["hexsha"]):
			self.summary = info["summary"]
			self.hexsha = info["hexsha"]
			self.action_confirm()
		else:
			self.action_quit()

	def action_quit(self):
		popup = ErrorPopup(
			self,
			"No Commit Selected",
			f"Select a commit from the timeline to {self.action}",
			500
		)
		destroyTogether(popup, self)

	def action_confirm(self):
		info = ""
		match self.action:
			case "revert":
				info = "Revert moves back to selected point and keeps the old commits (safe)"
				pass
			case "reset":
				info = "Reset moves back to selected point and removes the old commits (permanent)"

		question = f"Are you sure you want to perform an {self.action} on commit?"
		commit_data = f"Commit: {self.summary}\nHexsha: {self.hexsha[0:6]}"
		confirm = ConfirmationDialog(
			self,
			f"{question}\n\n{commit_data}\n\n{info}",
			"Continue",
			on_answer=self.action_confirm_reaction
		)

	def action_confirm_reaction(self, should_contine: bool, extra: str):
		if (should_contine):

			self.after(0,self.action_start)
		else:
			self.destroy()

	def action_start(self):
		self.popup = ForcedPopup(self,f"Performing {self.action}")
		self.popup.add_text(f"Starting {self.action}...")
		Thread(target=self.action_thread).start()
	
	def action_thread(self):
		result = "Nothing ran"
		match self.action:
			case "reset":
				result = reset(self.folder,self.hexsha)
			case "revert":
				result = revert(self.folder,self.hexsha)
		if not isinstance(result,str) and result is not None:
			self.action_cleanup()
		self.after(0,self.action_end,result)

	def action_cleanup(self):
		match self.action:
			case "revert":
				end_revert(self.folder)

	def action_end(self,result: None | str | GitError):
		if isinstance(result, str):
			self.popup.add_text(result)
			self.popup.add_text("Success!",tag="success")
			if self.onsuccess:
				self.onsuccess()
		elif result is not None:
			self.popup.add_text(result["title"],tag="error")
			self.popup.add_text(result["msg"],tag="error")
		self.popup.show_close(True)
