import sys
from src.window.tray import Tray
from src.media.image import logo_image
from src.window.manager import Manager
from src.core.colors import set_theme
import src.operations.project.storage as storage
import src.preferences.settings as settings

set_theme()
storage.load_app_list()
settings.load()
tray = Tray(logo_image)
manager = Manager()

tray.register_on_new(lambda: manager.new_window("Main"))
tray.register_on_quit(lambda: manager.close_all())

manager.mainloop()