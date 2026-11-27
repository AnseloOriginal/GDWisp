import math
import tkinter as tk
from tkinter import font
from typing import NotRequired, Text, TypedDict

import customtkinter as CTk
type Color = str | tuple[str,str] | None
class ConfigurableTextSetting(TypedDict):
	text: str
	size: NotRequired[int]
	color: NotRequired[Color]
	highlight: NotRequired[str]
	bold: NotRequired[bool]

class ConfigurableTextbox(tk.Text):
	def __init__(
		self, master,
		settings: list[ConfigurableTextSetting] | None = None, 
		update_size=False, background: Color = None, foreground: Color = None,
		**kwargs
	):
		super().__init__(
			master, 
			wrap="word", 
			background=take_one_str(background),
			foreground=take_one_str(foreground), 
			**kwargs)
		self.last_settings: list[ConfigurableTextSetting] = []
		if settings:
			self.load_texts(settings)
		if update_size:
			self.bind("<Configure>", lambda e: self.update_size())
			pass

	def load_texts(self,settings: list[ConfigurableTextSetting]):
		self.configure(state="normal")
		self.delete("1.0","end")
		for tag in self.tag_names():
			self.tag_delete(tag)
		for index, setting in enumerate(settings):
			tag_name = f"tag{index}"
			self.insert("end",setting["text"], tag_name)
			self.tag_config(
				tag_name, 
				foreground=take_one_str(setting.get("color")), 
				font=font.Font(
					family="Inter",
					size=setting.get("size") or -14,
					weight="bold" if setting.get("bold") else "normal",
				)
			)
		self.last_settings = settings.copy()
		self.update_size()
		self.configure(state="disabled")

	def add_texts(self, settings: list[ConfigurableTextSetting]):
		new_settings = self.last_settings + settings
		self.load_texts(new_settings)

	def update_size(self):
		if self.winfo_width() <= 1:  # not mapped yet, retry once it is
			self.after(50, self.update_size)
			return
		result = self.count("1.0", "end", "displaylines")
		lines = result[0] if result else 1
		if int(self.cget("height")) != lines:
			self.configure(height=max(lines, 1))
		# print(lines, self.cget("height"), self.winfo_height(),self.cget("wrap"),self.winfo_width())
		# self.update_idletasks()
		# text = self.get("1.0","end")
		# font = self._font
		# if isinstance(font,CTk.CTkFont):
		# 	line_height = font.metrics("linespace")
		# 	lines = math.ceil(font.measure(text) / self.winfo_reqwidth())
		# else:
		# 	line_height = font[1]
		# 	lines = 1
		# new_height = (line_height+(0.5*line_height))*lines
		# # print("Configurable Text: ",line_height,"Line Height:",new_height,lines,text[0:6])
		# self.grid_propagate(True)
		# self.master.grid_propagate(True)
		# self.master.update_idletasks()
		# self.configure(True, height=new_height)


def take_one_str(text: Color):
	if isinstance(text,str) or text is None:
		return text or "black"
	else:
		return text[0]


