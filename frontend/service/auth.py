from nicegui import app
from typing import Optional

user_sessions = {}

def get_current_user() -> Optional[dict]:
    session_id = app.storage.user.get("id")
    return user_sessions.get(session_id)