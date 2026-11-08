import src.preferences.settings as settings

def is_configured():
	s = settings.get_settings()
	if len(s.name.strip()) == 0 or len(s.email.strip()) == 0:
		return False
	else:
		return True
