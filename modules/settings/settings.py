from pydantic import ValidationError
from modules.settings.model import AppSettings
from modules.config.paths import folder_path
import json
import tempfile
import os

settings: AppSettings | None = None
setting_path = folder_path / "settings.json"

def load():
	global settings
	try:
		with open(setting_path, "r") as f:
			data = json.load(f)
		settings = AppSettings(**data)
		#how do I take my json into my settings
	except (FileNotFoundError, json.JSONDecodeError, ValidationError):
		settings = AppSettings()

def get_settings():
	if not settings:
		raise ValueError("Setting not loaded")
	return settings

def save_settings():
	if not settings:
		raise ValueError("Setting not loaded")
	temp_file_name = ""
	try:
		data = json.dumps(settings.model_dump())
		with tempfile.NamedTemporaryFile("w", dir=folder_path, delete=False) as temp_file:
			temp_file.write(data)
			temp_file_name = temp_file.name
		os.replace(temp_file_name,setting_path)
	except Exception as e:
		if os.path.exists(temp_file_name):
			os.remove(temp_file_name)
		raise e 
		# Do not close but crash as this is important
