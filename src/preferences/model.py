from src.core.paths import folder_path
from pydantic import Field, BaseModel
from typing import Literal
class AppSettings(BaseModel):
	name: str = Field(default="")
	email: str = Field(default="")
	theme: Literal["dark","light","system"] = Field(default="system")