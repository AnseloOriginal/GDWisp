import sys
import tkinter as tk
import logging, threading
from src.core.paths import folder_path
from logging.handlers import RotatingFileHandler

def setup_logging():
	log_path = folder_path / "gdwisp.log"
	file_handler = RotatingFileHandler(
		log_path,maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
	)
	console_handler = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter(
    	"[%(asctime)s] %(levelname)s [%(name)s:%(threadName)s] %(message)s"
	)
	file_handler.setFormatter(formatter)
	console_handler.setFormatter(formatter)
	root_logger = logging.getLogger()
	root_logger.setLevel(logging.INFO)
	root_logger.addHandler(file_handler)
	root_logger.addHandler(console_handler)
	threading.excepthook = handle_thread_exception
	sys.excepthook = handle_sys_exception
	tk.Tk.report_callback_exception = handle_tk_exception

def handle_sys_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception in main thread", exc_info=(exc_type, exc_value, exc_traceback))

def handle_thread_exception(args):
    thread_name = args.thread.name if args.thread else "Unknown Thread"
    logging.error(
        f"Uncaught exception in worker thread: {thread_name}", 
        exc_info=(args.exc_type, args.exc_value, args.exc_traceback)
    )

def handle_tk_exception(self, exc_type, exc_value, exc_traceback):
    logging.error(
        "Uncaught exception inside Tkinter callback", 
        exc_info=(exc_type, exc_value, exc_traceback)
    )