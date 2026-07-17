import customtkinter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from src.window.view import GUI_Functions

def view(app: customtkinter.CTkToplevel, funcs: "GUI_Functions", msg1: str, msg2: str):
  app.bell() 
  app.geometry("400x50")
  title = "Error has occured"  if type(msg1) != str else "Error: "+msg1
  app.title(title)
  app.resizable(False, True)
  app.grid_columnconfigure(0, minsize=10)
  label = customtkinter.CTkLabel(app, text=msg2, font=(None, 18), wraplength=400, justify="left")
  label.grid(row=0,column=1)
  app.focus()
  def close(event):
    if (event.widget == app):
      app.destroy()
  app.after(200, lambda: app.bind("<FocusOut>", close))
  def update():
    print("Error view cannot be updated")
  return update