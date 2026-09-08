import src.preferences.settings as settings

def is_configured():
	s = settings.get_settings()
	if s.name == "" or s.email == "":
		return False
	else:
		return True
