from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

    #schema for user login
class UserLogin(BaseModel):
    username: str
    password: str