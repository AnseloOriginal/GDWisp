import src.preferences.settings as settings
from src.core.colors import main_frame, theme_colors
import customtkinter as CTk

def labeled(parent,text: str,default: str):
	frame = CTk.CTkFrame(parent)
	label_text = CTk.CTkLabel(frame,text=text)
	textbox = CTk.CTkTextbox(frame, height=20)
	label_text.grid(column=0,row=0,padx=(20,0))
	textbox.grid(column=1,row=0,padx=10)
	return frame,textbox

class WelcomeMenu(CTk.CTkToplevel):

	def __init__(self,app) -> None:
		super().__init__(app)
		self.grab_set()
		self.title("Setup Message")
		self.geometry("400x300")
		self.resizable(False, False)
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)
		f = CTk.CTkFrame(self)
		f.configure(
			fg_color=main_frame["color"],
			border_color=main_frame["border_color"],
			border_width=main_frame["border_width"]
		)
		f.grid(column=0,row=0,padx=10,pady=10,sticky="nsew")
		label = CTk.CTkLabel(f,text="Welcome to Gdwisp. Let's get started.",font=(None,15,"bold"))
		label.grid(column=1,row=1,pady=(20,0),padx=(20,0))

		f1, name  = labeled(f,"Name:","")
		f2, email  = labeled(f,"Email:","")
		name.bind("<KeyRelease>", self.on_press)
		email.bind("<KeyRelease>", self.on_press)

		self.name = name
		self.email = email

		f1.grid(column=1,row=5,pady=(10,5))
		f2.grid(column=1,row=6,pady=(10,5))

		done_butn = CTk.CTkButton(f,width=75,height=40,text="Done",command=self.on_done)
		spacing = ((400-(2*10)) - 75) /2
		done_butn.grid(column=1,row=7,pady=(75,0),padx=spacing)
		done_butn.configure(state="disabled")
		self.done_butn = done_butn

		
	def on_press(self, evt):
		name = self.name.get("1.0","end")
		email = self.email.get("1.0","end")
		if name.lstrip() == "" or email.lstrip() == "":
			self.done_butn.configure(state="disabled")
		else:
			self.done_butn.configure(state="normal")


	def on_done(self):
		name = self.name.get("1.0","end").rstrip()
		email = self.email.get("1.0","end").rstrip()
		s = settings.get_settings()
		s.name = name
		s.email = email
		settings.save_settings()
		self.destroy()
