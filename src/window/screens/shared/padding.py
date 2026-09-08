import customtkinter

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
