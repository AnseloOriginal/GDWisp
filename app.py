import sys
from modules.window.tray import Tray
from modules.media.image import logo_image
from modules.window.manager import Manager


tray = Tray(logo_image)
manager = Manager()

tray.register_on_new(lambda: manager.new_window())
tray.register_on_quit(lambda: manager.close_all())

manager.mainloop()

