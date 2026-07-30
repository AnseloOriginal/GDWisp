from threading import Thread
from typing import Literal
import customtkinter as CTk

from src.operations.git.types import GitError
from src.window.screens.shared.buttons import multiple_button
from src.operations.git.stash import get_all_stash, pop_stash
from src.window.screens.shared.error_popup import ErrorPopup

type modes = Literal["restore"]

class StashTool(CTk.CTkToplevel):
	def __init__(self,parent, type: modes, folder: str):
		super().__init__(parent)
		self.folder = folder
		self.grab_set()
		self.render()
		self.stash_list: list[tuple[str,str]] = []
		Thread(target=self.collect_info).start()

	def render(self):
		self.grid_columnconfigure(0, weight=1)
		label = CTk.CTkLabel(self,text="Select a stash/save to restore it")
		self.stashes = CTk.CTkOptionMenu(self,values=[""])
		frame, buttons = multiple_button(self,"Restore","Cancel")
		self.stashes.configure(state="disabled")
		buttons[0].configure(state="disabled")
		buttons[0].configure(
			command=self.action_start
		)
		buttons[1].configure(
			command = lambda: self.destroy()
		)
		self.restore_butn = buttons[0]
		self.cancel_butn = buttons[1]
		label.grid(column=0,row=0,pady=(20,0),padx=20,sticky="ew")
		self.stashes.grid(column=0,row=1,pady=10,padx=20,sticky="ew")
		frame.grid(column=0,row=2,pady=10,padx=20,sticky="ew")

	def action_start(self):
		current = self.stashes.get()
		stash_id: str | None = None
		for stash in self.stash_list:
			if current == stash[1]:
				stash_id = stash[0]
				break
		if not stash_id:
			return
		self.stashes.configure(state="disabled")
		self.restore_butn.configure(state="disabled")
		self.cancel_butn.configure(state="disabled")
		Thread(target=self.action_thread,args=[stash_id]).start()

	def action_thread(self, stash_id: str):
		results = pop_stash(self.folder,stash_id)
		self.after(0, self.action_end, results)

	def action_end(self, results: GitError | str | None):
		if isinstance(results,str) or results == None:
			self.destroy()
		else:
			ErrorPopup(self,results["title"],results["msg"])
		
	def collect_info(self):
		stashes = get_all_stash(self.folder)
		self.after(0, self.update_info, stashes)

	def update_info(self, stashes: list[tuple[str,str]] ):
		if len(stashes) > 0:
			viewable_list = [r[1] for r in stashes]
			self.stashes.configure(values=viewable_list)
			self.restore_butn.configure(state="normal")
			self.stashes.configure(state="normal")
			self.stash_list = stashes





