import sys
from modules.window.tray import Tray
from modules.media.image import logo_image
from modules.window.manager import Manager
from modules.config.colors import set_theme
import modules.operations.project.storage as storage
import modules.settings.settings as settings

set_theme()
storage.load_app_list()
settings.load()
tray = Tray(logo_image)
manager = Manager()

tray.register_on_new(lambda: manager.new_window("Main"))
tray.register_on_quit(lambda: manager.close_all())

manager.mainloop()

