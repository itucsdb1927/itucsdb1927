from dataclasses import dataclass

from .base_model import BaseModel

@dataclass
class User(BaseModel):
    creator: int
    image_file: str
    username: str
    email_address: str
    password: str
    first_name: str
    last_name: str
    is_admin: bool
