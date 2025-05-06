from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "jobseeker"  # default