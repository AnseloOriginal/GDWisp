import customtkinter
from src.core.colors import status_colors

class ForcedPopup(customtkinter.CTkToplevel):
  def __init__(self, parent: customtkinter.CTk | customtkinter.CTkToplevel, title:str="", **args):
    super().__init__(parent,**args)
    self.geometry("400x260")
    self.title(title)
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
