# from jose import JWTError, jwt
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from app import schemas, models, database
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from typing import Optional

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY = "your_secret_key_here"  # Replace with your actual secret key
# ALGORITHM = "HS256"  # Or your preferred algorithm

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         role = payload.get("role")
#         token_data = schemas.TokenData(email=email, role=role)

#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = db.query(models.User).filter(models.User.email == token_data.email).first()
#     if user is None:
#         raise credentials_exception
#     return user

# class TokenData(BaseModel):
#     email: Optional[str] = None
#     role: Optional[str] = None


# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# access_token = create_access_token(data={"sub": user.email, "role": user.role})
# class TokenData(BaseModel):
#     email: Optional[str] = None
#     role: Optional[str] = None

# # inside get_current_user:
# payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# email = payload.get("sub")
# role = payload.get("role")
# token_data = schemas.TokenData(email=email, role=role)
# def require_role(required_role: str):
#     def role_checker(current_user: models.User = Depends(get_current_user)):
#         if current_user.role != required_role:
#             raise HTTPException(status_code=403, detail="Insufficient permissions")
#         return current_user
#     return role_checker
# @router.get("/admin/dashboard")
# def admin_dashboard(current_user: models.User = Depends(require_role("admin"))):
#     return {"msg": f"Welcome Admin {current_user.username}"}


from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app import schemas, models, database
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "your_secret_key_here"  # Replace with actual secret
ALGORITHM = "HS256"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role = payload.get("role")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: str):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker


