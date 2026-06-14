import customtkinter
from modules.media.image import ICON
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
    hover_colors=(None, None),
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
    hover_color=hover_colors,
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
  hover_colors=(None, None),
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
    fake_butn.configure(fg_color=hover_colors)

  def on_unhover(event):
    fake_butn.configure(fg_color=butn_color)
    
  
  def on_click(event):
    fake_butn.after(100,lambda: fake_butn.configure(fg_color=butn_color))
    fake_butn.after(200,lambda: fake_butn.configure(fg_color=hover_colors))
    if (onclick):
      onclick()
      
  def binder(*childs: customtkinter.CTkBaseClass):
    for child in childs:
      child.bind("<Enter>", on_hover, add="+")
      child.bind("<Leave>",on_unhover,add="+")
      child.bind("<Button-1>",on_click,add="+")
  
  binder(fake_butn,main_label,small_label)

  return fake_butn
  