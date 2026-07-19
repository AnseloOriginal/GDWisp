import customtkinter as CTk

class ErrorPopup(CTk.CTkToplevel):
  def __init__(self,parent, msg1: str, msg2: str):
    super().__init__(parent)
    self.bell() 
    self.geometry("400x50")
    title = "Error has occured" if type(msg1) != str else "Error: "+msg1
    self.title(title)
    self.resizable(False, True)
    self.grid_columnconfigure(0, minsize=10)
    label = CTk.CTkLabel(self, text=msg2, font=(None, 18), wraplength=400, justify="left")
    label.grid(row=0,column=1)
    self.focus()
    def close(event):
      if (event.widget == self):
        self.destroy()
    self.after(200, lambda: self.bind("<FocusOut>", close))
    