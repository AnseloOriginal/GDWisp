from time import sleep
from typing import Literal
import customtkinter as CTk
from src.window.screens.shared.buttons import multiple_button
import src.operations.git.remotes as git_remotes
from threading import Thread
from src.window.screens.shared.error_popup import ErrorPopup

type modes = Literal["create","delete"]

mode_name: dict[modes, str] = {
	"create": "Create",
	"delete": "Delete"
}

mode_sizes: dict[modes, str] = {
	"create": "350x150",
	"delete": "350x150"
}

mode_confirm: dict[modes, str] = mode_name

plural_modes: list[modes] = []

class RemoteTool(CTk.CTkToplevel):
	def __init__(self,app,mode: modes, folder: str):
		super().__init__(app)
		self.grab_set()
		self.title(
			f"{mode_name[mode]} remote{"es" if mode in plural_modes else ""}"
		)
		self.folder = folder
		self.textboxes: list[CTk.CTkEntry] = []
		self.options: list[CTk.CTkOptionMenu] = []
		self.geometry(mode_sizes[mode])
		self.resizable(False,False)
		self.grid_columnconfigure(1, weight=1)
		self.mode: modes = mode
		self.closable = True
		self.remotes: list[str] | None = None;
		self.result: Literal[True] | git_remotes.Error | None = None

		options, buttons = multiple_button(self,mode_confirm[mode],"Cancel")
		buttons[0].configure(command=self.action_start, state="disabled")
		buttons[1].configure(command=self.close)

		self.confirm_butn = buttons[0]
		self.close_butn = buttons[1]
		self.row = 1
		self.grid_rowconfigure(5, minsize=50)
		self.grid_rowconfigure(0, minsize=10)
		self.grid_columnconfigure((0,2), minsize=20)
		options.grid(column=1,row=6, sticky="nsew")
		self.setup()

	def close(self):
		if self.closable:
			self.destroy()

	def action_start(self):
		self.closable = False
		self.close_butn.configure(state="disabled")
		self.confirm_butn.configure(state="disabled")
		for items in self.options:
			items.configure(state="disabled")

		for items in self.textboxes:
			items.configure(state="disabled")
		Thread(target=self.action_execute).start()

	def action_execute(self):
		self.result = self.action_execute_mode()
		self.after(0, self.action_end)

	def action_execute_mode(self):
		match self.mode:
			case "create":
				name = self.text_value(0)
				url = self.text_value(1)
				if not name or not url:
					return None
				return git_remotes.add_remote(self.folder,name,url)
			case "delete":
				name = self.text_value(0)
				if not name:
					return None
				return git_remotes.delete_remote(self.folder,name)

	def action_end(self):
		if self.result == True:
			self.destroy()
			return
		elif self.result == None:
			ErrorPopup(
				self,
				f"Failed {self.mode}",
				"Failed due to unknown reasons"
			)
		else:
			ErrorPopup(
				self,
				self.result["title"],
				self.result["msg"]
			)

	def setup(self):
		match self.mode:
			case "create":
				self.add_textbox("Name")
				self.add_textbox("Url")
			case "delete":
				self.add_remote_option("Remote")
				self.add_textbox("Confirm",placeholder="Type Remote Name to Confirm")
		if len(self.options) > 0:
			Thread(target=self.fetch_remotes).start()

	def validate(self, evt_or_choice):
		result = self.mode_validate()
		mode = "active" if result else "disabled"
		self.confirm_butn.configure(state=mode)

	def mode_validate(self) -> bool | None:
		match self.mode:
			case "create":
				return self.text_entered(0) and self.text_entered(1)
			case "delete":
				name = self.text_value(0)
				remote = self.option_value(0)
				return name != "" and name != None and name == remote
			
	def add_textbox(self,label:str,placeholder=None):
		frame = CTk.CTkFrame(self)
		frame.grid_columnconfigure(1,weight=1)
		label_text = CTk.CTkLabel(frame,text=label, anchor="w")
		textbox = CTk.CTkEntry(frame, height=25,placeholder_text=placeholder)
		label_text.grid(column=0,row=0)
		textbox.grid(column=1,row=0,padx=(10,0),sticky="ew")
		textbox.bind("<KeyRelease>", self.validate)
		frame.grid(column=1,row=self.row,sticky="nsew")
		self.row += 1
		self.textboxes.append(textbox)

	def add_remote_option(self,label: str):
		frame = CTk.CTkFrame(self)
		frame.grid_columnconfigure(1,weight=1)
		label_text = CTk.CTkLabel(frame,text=label, anchor="w")
		option = CTk.CTkOptionMenu(frame, height=25,values=[""],command=self.validate)
		label_text.grid(column=0,row=0)
		option.grid(column=1,row=0,padx=(10,0),sticky="ew")
		frame.grid(column=1,row=self.row,sticky="nsew")
		self.configure_option(option)
		self.row += 1
		self.options.append(option)

	def configure_option(self, option: CTk.CTkOptionMenu):
		if self.remotes:
			option.option_clear()
			option.configure(values=self.remotes)
			option.configure(state="active")
		else:
			option.configure(state="disabled")

	def text_value(self,id: int):
		if id < len(self.textboxes):
			return self.textboxes[id].get()
		else:
			return None

	def option_value(self,id: int):
		if id < len(self.options):
			return self.options[id].get()
		else:
			return None
	
	def text_entered(self,id: int):
		if id < len(self.textboxes):
			text = self.textboxes[id].get()
			return len(text) > 0
		else:
			return False
	
	def option_picked(self,id: int):
		if id < len(self.options):
			return len(self.options[id].get()) > 0
		else:
			return False

	def update_remotes(self):
		for option in self.options:
			self.configure_option(option)

	def fetch_remotes(self):
		remotes = git_remotes.get_remotes(self.folder)
		self.remotes = remotes
		print("Updating remotes",self.remotes)
		self.after(0, self.update_remotes)