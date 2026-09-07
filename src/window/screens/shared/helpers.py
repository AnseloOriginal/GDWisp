from sys import maxsize, prefix

import customtkinter
from src.media.image import ICON
from src.core.colors import status_colors
from typing import Callable


class AutoHidingScrollFrame(customtkinter.CTkScrollableFrame):

  def __init__(self, master: customtkinter.CTkBaseClass, **kwargs):
    self._scrollbar_visible = True
    super().__init__(master,**kwargs)
    self.bind("<Configure>", self.check_scrollbar, add="+")

  def check_scrollbar(self,event):
    self.update_idletasks()
    viewport_height = self._parent_canvas.winfo_height()
    content_height = self.winfo_reqheight()
    needs_scrollbar = content_height > viewport_height
    if needs_scrollbar == self._scrollbar_visible:
        return
    self._scrollbar_visible = needs_scrollbar
    if needs_scrollbar:
        self._scrollbar.grid()
    else:
        self._scrollbar.grid_remove()


class LabeledText(customtkinter.CTkFrame):

  def __init__(self,parent, labelText: str, preText: str, spacing: int = 100,  **kwargs):
    super().__init__(parent, height=15,  **kwargs)
    
    self.label = customtkinter.CTkLabel(self, height=15, text=labelText+":", font=(None, 14, "bold"), anchor="w")
    self.text = customtkinter.CTkLabel(self, height=15, text=preText, font=(None, 14), anchor="w")
    self.label.grid(column=0,row=0,sticky="ew")
    self.spacing = spacing
    self.grid_columnconfigure(1,minsize=spacing)
    self.text.grid(column=2, row=0,sticky="ew")
    self.after(500, self.update_spacing)
    

  def change_text(self,text:str):
    self.text.configure(text=text)

  def update_spacing(self):
    size = self.label.winfo_width()
    self.grid_columnconfigure(1,minsize=(self.spacing-size))


class AdvancePadding(customtkinter.CTkFrame):
  
  def __init__(self,parent,headerText: str, padding: int=40, **kwargs):
    """ Always use column 1 and above for padded """
    super().__init__(parent, **kwargs)
    self.heading = customtkinter.CTkLabel(self, text=headerText, font=(None, 18, "bold"), anchor="w")
    self.heading.grid(column=0,row=0,sticky="nw")
    self.padded = customtkinter.CTkFrame(self,height=0)
    self.nonpadded = customtkinter.CTkFrame(self,height=0)
    self.padded.grid(column=0,row=1,sticky="ew")
    self.nonpadded.grid(column=0,row=2,sticky="ew")
    self.padded.grid_columnconfigure(0,minsize=padding)

  def autogrid(self, *widgets: customtkinter.CTkBaseClass, spacing=0):
    n = 0
    for widget in widgets:
      widget.grid(column=1,row=n,sticky="ew",pady=spacing)
      n+=1

def safe_get[T, D](lst: list[T], index: int, default: D = None) -> T | D:
    try:
        return lst[index]
    except IndexError:
        return default