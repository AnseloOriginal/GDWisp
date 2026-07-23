from queue import Queue
from threading import Thread

import customtkinter as CTk
from typing import Literal, Callable
from src.window.screens.shared.forced_popup import ForcedPopup
from src.window.screens.shared.buttons import multiple_button
from src.operations.git.remotes import get_remotes
import src.operations.git.sync as git_sync

type modes = Literal["pull","push","sync","link"]
type on_remote_dialog_selection = Callable[[Literal["yes","no"], str], None]

class RemoteDialogSelection(CTk.CTkToplevel):

	def __init__(self, parent,  folder: str, on_choice: on_remote_dialog_selection):
		super().__init__(parent)
		self.grab_set()
		self.folder = folder
		self.remotes: list[str] | None = None
		self.title("Select Remote")
		self.geometry("300x125")
		self.resizable(False,False)
		self.on_choice = on_choice
		self.sent = False
		self.build_ui()
		Thread(target=self.fetch_remotes).start()

	def build_ui(self):
		self.grid_columnconfigure(0,weight=1)
		text = CTk.CTkLabel(self, text="Select a remote/server to push to")
		self.option = CTk.CTkOptionMenu(self, values=[""], state="disabled", command=self.validate)
		options, buttons = multiple_button(self,"Done","Cancel")
		self.done_butn = buttons[0]
		self.done_butn.configure(state="disabled")
		text.grid(column=0,row=0,padx=20,pady=(10,0),sticky="ew")
		self.option.grid(column=0,row=1,pady=(5,0))
		options.grid(column=0,row=2,padx=20,pady=(10,0),sticky="ew")
		buttons[0].configure(
			command=lambda: self.yes(self.option.get())
		)
		buttons[1].configure(
			command=lambda: self.no()
		)
		self.bind("<Destroy>",lambda evt: self.cleanup(evt))

	def yes(self,remote: str):
		self.on_choice("yes", remote)
		self.sent = True
		self.destroy()
		
	def no(self):
		self.on_choice("no","")
		self.sent = True
		self.destroy()
		
	def cleanup(self,evt):
		if not self.winfo_exists():
			return
		if evt.widget == self and not self.sent:
			self.on_choice("no","")

	def fetch_remotes(self):
		remotes = get_remotes(self.folder)
		self.remotes = remotes
		print("Updating remotes",self.remotes)
		self.after(0, self.update_remotes)

	def update_remotes(self):
		if not self.remotes or len(self.remotes) == 0:
			return
		self.option.configure(
			state="active",
			values=self.remotes
		)

	def validate(self, option: str):
		if len(option) > 0:
			self.done_butn.configure(state="active")






class SyncTool(CTk.CTkToplevel):
	def __init__(self, parent, folder: str, mode: modes) -> None:
		super().__init__(parent)
		self.grab_set()
		self.mode = mode
		self.folder = folder
		self.withdraw()
		self.remote: str | None
		self.action_prepare()

	def action_prepare(self):
		is_instant = self.action_prepare_mode()
		if is_instant:
			self.action_execute()
		else:
			self.get_choice_first()

	def action_prepare_mode(self):
		match self.mode:
			case "link":
				return False
			case "sync":
				return True
			case "pull":
				return True
			case "push":
				return True

	def get_choice_first(self):
		def results(choice: Literal["yes","no"], remote: str):
			if choice == "no":
				print("User canceled")
				self.destroy()
			else:
				print("Going with",remote)
				self.remote = remote
				self.action_execute()
		dialog = RemoteDialogSelection(self,self.folder,results)

	def action_execute(self):
		self.popup = ForcedPopup(self,title=f"Launch {self.mode}")
		self.queue = Queue()
		Thread(target=self.action_execute_thread).start()
		self.action_announce()

	def action_announce(self):
		match self.mode:
			case "pull":
				self.popup.add_text("Started pull operation.")
			case "push":
				self.popup.add_text("Started push operation.")
			case "link":
				self.popup.add_text(f"Linking Remote {self.remote}")
				self.popup.add_text("Started pull operation.")
			case "sync":
				self.popup.add_text("Started sync procedure.")
				
	def action_execute_thread(self):
		result = "Nothing ran"
		progress = git_sync.ProgressUpdate(
			lambda msg: self.send_msg_from_thread(msg)
		)
		match self.mode:
			case "pull":
				result = git_sync.pull(self.folder,progress=progress)
			case "push":
				result = git_sync.push(self.folder,None,progress=progress)
			case "link":
				result = git_sync.push(self.folder,self.remote,progress=progress)
			case "sync":
				result = git_sync.pull(self.folder,progress=progress)
				if result == True:
					self.send_msg_from_thread("Started push operation")
					result = git_sync.push(self.folder,None,progress=progress)
		self.queue.put(result)
		self.after(0, self.action_end)

	def send_msg_from_thread(self, msg: str):
		if not self.popup or not msg.strip():
			return
		self.after(0, lambda: self.popup.add_text(msg))

	def action_end(self):
		results = self.queue.get()
		if type(results) is str:
			self.popup.add_text(results,tag="success")
		elif isinstance(results,dict):
			self.popup.add_text(results.get("title","Unknown Crash"),tag="error")
			self.popup.add_text(results.get("msg","Unknown Crash Error"),tag="error")
		self.popup.show_close(True)
		





