from sys import maxsize, prefix

import customtkinter
from modules.media.image import ICON
from modules.config.colors import status_colors
from typing import Callable

def create_icon_butn(
    parent: customtkinter.CTkFrame, text: str, 
    icon: str, text_color: tuple,
    butn_color: tuple,
    col: int, row: int,
    width: int = 200,
    height: int = 40,
    font_size: int=20,
    pady=5,
    padx=0,
    hover_color=None,
    command=None
  ): 
  """Creates a Ctk button with an icon"""
  image = customtkinter.CTkImage(ICON[icon])
  butn = customtkinter.CTkButton(
    parent, 
    text=text,
    text_color = text_color,
    fg_color= butn_color,
    image= image,
    compound="left",
    width=width,
    height=height,
    font=(None,font_size),
    hover_color=hover_color,
    command=command
  )
  butn.grid(row=row, column=col, pady=pady)
  return butn

def create_project_butn(
  parent: customtkinter.CTkFrame,
  main_text: str, small_text: str,
  main_text_color: tuple, butn_color: tuple, small_text_color: tuple,
  col: int, row: int,
  main_font_size=20, small_font_size=10,
  width: int = 200, height: int = 500,
  pady=5, padx=0,
  hover_color=None,
  sticky="nsew",
  onclick: Callable[[], None] = lambda: print("No handler registered")
): 
  """Creates a custom button using CTkFrame"""
  fake_butn = customtkinter.CTkFrame(parent, fg_color=butn_color, width=width, height=height)
  fake_butn.grid(column=col, row=row, padx=padx, pady=pady, sticky=sticky)
  fake_butn.grid_columnconfigure(0,minsize=10)
  fake_butn.grid_columnconfigure(3,minsize=10)
  fake_butn.grid_columnconfigure(2,weight=1)
  main_label = customtkinter.CTkLabel(fake_butn, text=main_text, font=(None,main_font_size), text_color=main_text_color)
  main_label.grid(column=1,row=1)
  small_label = customtkinter.CTkLabel(fake_butn, text=small_text, font=(None,small_font_size), text_color=small_text_color)
  small_label.grid(column=2,row=1, sticky='se')
  def on_hover(event):
    fake_butn.configure(fg_color=hover_color)

  def on_unhover(event):
    fake_butn.configure(fg_color=butn_color)
    
  
  def on_click(event):
    fake_butn.after(100,lambda: fake_butn.configure(fg_color=butn_color))
    fake_butn.after(200,lambda: fake_butn.configure(fg_color=hover_color))
    if (onclick):
      onclick()
      
  def binder(*childs: customtkinter.CTkBaseClass):
    for child in childs:
      child.bind("<Enter>", on_hover, add="+")
      child.bind("<Leave>",on_unhover,add="+")
      child.bind("<Button-1>",on_click,add="+")
  
  binder(fake_butn,main_label,small_label)

  return fake_butn
  
class AutoHidingScrollFrame(customtkinter.CTkScrollableFrame):

  def __init__(self, master: customtkinter.CTkBaseClass, **kwargs):
    self._scrollbar_visible = True
    super().__init__(master,**kwargs)
    self.bind("<Configure>", self.check_scrollbar, add="+")

  def check_scrollbar(self,event):
    self.update_idletasks()
    viewport_height = self._parent_canvas.winfo_height()
    content_height = self.winfo_reqheight()
    print(content_height,viewport_height)
    needs_scrollbar = content_height > viewport_height
    if needs_scrollbar == self._scrollbar_visible:
        return
    self._scrollbar_visible = needs_scrollbar
    if needs_scrollbar:
        self._scrollbar.grid()
    else:
        self._scrollbar.grid_remove()

class ForcedPopup(customtkinter.CTkToplevel):
  def __init__(self, parent: customtkinter.CTk | customtkinter.CTkToplevel, *args):
    super().__init__(parent,*args)
    self.geometry("400x260")
    self.grab_set()
    self.attributes("-topmost", True)
    self.protocol("WM_DELETE_WINDOW", lambda: None)
    self.resizable(width=False,height=False)
    self.grid_rowconfigure((0,2,4), minsize=10)
    self.grid_columnconfigure((0,2), minsize=10)
    self.grid_columnconfigure(1, weight=1)
    self._render()
    self.textbox.configure(state="disabled")
    for name in status_colors.keys():
      self.textbox.tag_config(name, foreground=status_colors[name])
    self.show_close(False)

  def _render(self):
    self.textbox = customtkinter.CTkTextbox(self,height=200)
    self.textbox.grid(column=1,row=1,sticky="ew")
    self.close_butn = customtkinter.CTkButton(self,text="Close", command=self.destroy)
    self.close_butn.grid(column=1,row=3)
    pass

  def add_text(self,text:str,newline: bool=True, tag=None):
    self.textbox.configure(state="normal")
    self.textbox.insert("end", "\n"+text if newline else text, tag)
    self.textbox.configure(state="disabled")

  def close(self):
    self.destroy()

  def show_close(self, show: bool):
    if (show):
      self.close_butn.configure(state="normal")
    else:
      self.close_butn.configure(state="disabled")

def multiple_button(parent,*labels: str, minsize: int = 25):
  frame = customtkinter.CTkFrame(parent)
  buttons: list[customtkinter.CTkButton] = []
  n = 0
  for label in labels:
    button = customtkinter.CTkButton(frame,text=label)
    button.grid(row=0,column=n,sticky="ew")
    frame.grid_columnconfigure(n,weight=2)
    buttons.append(button)
    gap_col  = n - 1
    if (n >= 1):
        frame.grid_columnconfigure(gap_col,minsize=minsize,weight=1)
    n = n + 2
  return frame,buttons

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

