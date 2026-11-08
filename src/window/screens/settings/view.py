import customtkinter as CTk
from typing import TYPE_CHECKING, Literal, cast
from src.preferences import settings
from src.window.screens.shared.labelled_text import labeled

if TYPE_CHECKING:
  from src.window.view import GUI_Functions

def view(view: CTk.CTkToplevel, funcs: "GUI_Functions"):
	current_settings = settings.get_settings()
	view.title("GDWisp Settings")
	view.geometry("400x300")
	view.columnconfigure(0,weight=1)
	view.resizable(False,False)
	inter_font = CTk.CTkFont(family='Inter', size=14, weight="bold")

	app_mode_label = CTk.CTkLabel(view,text="Appearance",font=inter_font)
	app_mode_label.grid(row=0,column=0,pady=(10,0),padx=(20,0))
	app_mode = CTk.CTkSegmentedButton(
		view,values=["System","Light","Dark"],command=change_mode,
		height=40
	)
	app_mode.set(current_settings.theme.capitalize())
	app_mode.grid(row=1,column=0,pady=(5,0),padx=30,sticky="ew")

	git_info = CTk.CTkFrame(view)
	f1, git_info_name  = labeled(git_info,"Name:",current_settings.name)
	f2, git_info_email  = labeled(git_info,"Email:",current_settings.email)
	update_git_info = lambda evt: change_git_info(
		git_info_name.get("1.0","end"),
		git_info_email.get("1.0","end")
	)
	git_info_name.bind("<KeyRelease>", update_git_info)
	git_info_email.bind("<KeyRelease>", update_git_info)
	git_info.grid(row=2,column=0,pady=(20,0),padx=30,sticky="ew")
	f1.grid(column=1,row=5)
	f2.grid(column=1,row=6,pady=(10,0))

def change_mode(selected: str):
	CTk.set_appearance_mode(selected.lower())
	settings.get_settings().theme = cast(
		Literal["system","light","dark"],
		selected.lower()
	)
	settings.save_settings()

def change_git_info(name: str, email: str):
	current_settings = settings.get_settings()
	current_settings.name = name.strip()
	current_settings.email = email.strip()
	settings.save_settings()