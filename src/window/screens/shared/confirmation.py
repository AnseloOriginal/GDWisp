from tkinter import Event

import customtkinter as CTk
from typing import Callable

from src.window.screens.shared.buttons import multiple_button

class ConfirmationDialog(CTk.CTkToplevel):
	def __init__(
		self,
		parent,
		text: str, 
		*buttons: str, 
		on_answer: Callable[[bool,str], None],
		title = "Confirmation"
	):
		super().__init__(parent)
		self.title(title)
		self.grab_set()

		self.grid_columnconfigure(0, weight=1)
		label = CTk.CTkLabel(self,text=text)
		label.grid(column=0,row=0,pady=10,padx=10,sticky="ew")

		frame, b1 = multiple_button(self, *buttons, "Cancel")
		frame.grid(column=0,row=1,padx=10,pady=10,sticky="ew")

		def on_click(button: CTk.CTkButton):
			text = button.cget("text")
			if text == "Cancel":
				on_answer(False,text)
			else:
				on_answer(True,text)
			self.destroy()

		for button in b1:
			button.configure(
				command = lambda b=button: on_click(b)
			)




