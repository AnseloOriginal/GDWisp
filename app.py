import sys
import shutil
from src.window.tray import Tray
from src.media.image import logo_image
from src.window.manager import Manager
from src.core.colors import set_theme
import src.operations.project.storage as storage
import src.preferences.settings as settings
from tkinter import messagebox

def start_app():
	set_theme()
	storage.load_app_list()
	settings.load()
	tray = Tray(logo_image)
	manager = Manager()

	tray.register_on_new(lambda: manager.new_window("Main"))
	tray.register_on_quit(lambda: manager.close_all())

	manager.mainloop()

def pre_check():
	GIT_INSTALLED = shutil.which("git")
	if GIT_INSTALLED:
		start_app()
	else:
		response = messagebox.askokcancel(
	    	"Git not found", 
	    	"Git is not installed on the machine. Please install git to use GDWisp",
	    	icon='error' # Keeps the error styling
		)
		if response:
			import webbrowser
			webbrowser.open("https://git-scm.com")
		else:
			pass

pre_check()