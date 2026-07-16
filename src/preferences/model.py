from src.core.paths import folder_path
from pydantic import Field, BaseModel

class AppSettings(BaseModel):
	name: str = Field(default="")
	email: str = Field(default="")