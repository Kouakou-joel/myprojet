from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    disabled: bool

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None
    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: str 
    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str

class UserResponse(BaseModel):
    id: int
    list: Optional[User]
    class Config:
        from_attributes = True

