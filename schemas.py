"""Fields for creating, editing, and showing a user."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=120)


class UserOutput(UserInput):
    model_config = ConfigDict(from_attributes=True)
    id: int
