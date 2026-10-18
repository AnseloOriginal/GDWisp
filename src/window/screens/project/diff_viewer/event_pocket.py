import customtkinter as CTk

class EventPocket(CTk.CTkFrame):
	def  __init__(self,master, **kwargs):
		super().__init__(master,**kwargs)
		self.columnconfigure(0,weight=1)
		self.collasped = False
		self.butn = CTk.CTkButton(self,command=self.toggle_state)
		self.pocket_space = CTk.CTkFrame(self)
		self.butn.columnconfigure(0, weight=1)
		self.butn.grid(column=0,row=0,sticky="ew")
		self.pocket: list[CTk.CTkBaseClass] = []

	def add(self, widget: CTk.CTkBaseClass):
		self.pocket.append(widget)
		self.update_text()
		if self.collasped:
			widget.grid()
		else:
			widget.grid_remove()

	def update_text(self):
		if self.collasped:
			self.butn.configure(
				text="Click to hide events"
			)
		else:
			count = len(self.pocket)
			self.butn.configure(
				text=f"{count} Event{"s" if count > 0 else ""} hidden. Click to show events."
			)

	def toggle_state(self):
		if self.collasped:
			for widget in self.pocket:
				widget.grid_remove()
			self.collasped = False
		else:
			for widget in self.pocket:
				widget.grid()
			self.collasped = True




