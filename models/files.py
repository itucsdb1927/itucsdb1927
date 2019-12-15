from dataclasses import dataclass

from models.base_model import BaseModel


@dataclass
class ImageFile(BaseModel):
    is_local: bool
    path: str


@dataclass
class AudioFile(BaseModel):
    is_local: bool
    path: str
