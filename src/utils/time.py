from datetime import datetime, timezone, time

def current_time():
  return datetime.now(timezone.utc).strftime("%I:%M%p, %d %B %Y").lstrip("0")