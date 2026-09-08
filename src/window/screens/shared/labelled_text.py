import customtkinter

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
