from .models import User
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class UserSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=255, description="first_name is required!")
    other_names: str = Field(..., min_length=1, max_length=255, description="other_names is required!")
    email: EmailStr = Field(..., description="A valid email is required!")
    username: str = Field(..., min_length=4, max_length=32, description="username must be 4-32 characters long.")
    password: str = Field(..., min_length=8, max_length=32, description="password must be 8-32 characters long.")

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("password must include at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValueError("password must include at least one number.")
        if not re.search(r"[!@#$%^&*()_+-=]", value):
            raise ValueError("password must include at least one special character.")
        return value

    @field_validator("email")
    def validate_email(cls, value):
        if User.objects.filter(email=value).exists():
            raise ValueError("email is already in use!")
        return value

    @field_validator("username")
    def validate_username(cls, value):
        if User.objects.filter(username=value).exists():
            raise ValueError("username is already in use!")
        return value
    
class LoginSchema(BaseModel):
    identifier: str = Field(..., description="first_name is required!")
    password: str = Field(..., description="other_names is required!")
    
    


class JobSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="title is required!")
    company: str = Field(..., min_length=3, max_length=100, description="company is required!")
    location: str = Field(..., min_length=3, max_length=100, description="location is required!")
    description: str = Field(..., description="description is required!")
    category: Optional[str] = None
    
class JobApplicaitonSchema(BaseModel):
    cover_letter: str = Field(..., description="cover_letter is required!")