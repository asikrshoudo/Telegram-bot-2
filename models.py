# Database models
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Group:
    id: int
    group_id: str
    group_name: str
    welcome_msg: str = "👋 Welcome {user} to {group}!"
    rules_msg: str = "Be respectful!"
    is_active: bool = True
    created_at: datetime = None

@dataclass
class Promotion:
    id: int
    user_id: int
    message: str
    photo_id: str = None
    status: str = "pending"
    sent_to: int = 0
    created_at: datetime = None