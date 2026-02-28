from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
import models, schemas,utilis
from auth_database import get_db
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


SECRET_KEY = "4ea8b89b715dadf4491c95fd27c6cdc6018fe01076757a3ab2dc975d37836c4a"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#helper function that takes user data
def create_access_token(data: dict):
    to_encode = data.copy()
    expire= datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.user).filter((models.user.username == user.username) | (models.user.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    hashed_password = utilis.hash_password(user.password)
    new_user = models.user(username=user.username,
                            email=user.email, 
                            password_hash=hashed_password,
                            role=user.role)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email, 'role': new_user.role}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.username == form_data.username).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if not utilis.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid  password")    
    
    token_data = {"sub": user.username, "role": user.role}
    token = create_access_token(token_data) 
    return {"access_token": token, "token_type": "bearer"}  