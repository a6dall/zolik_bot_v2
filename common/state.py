"""Общее «состояние» между Telegram- и Discord-ботами."""
from typing import Set, Optional

class BotState:
    chat_id:      Optional[int] = None
    message_id:   Optional[int] = None
    caller_id:    Optional[int] = None
    caller_name:  Optional[str] = None
    coming:       Set[str] = set()
    busy:         Set[str] = set()
    muted_since: dict[int, float] = {}  # когда пользователь замьютился
    afk: set[int] = set()  # кто уже считается AFK

STATE = BotState()
