from fastapi import FastAPI, HTTPException
from app.auth_service import (
    create_user,
    authenticate_user,
    UserAlreadyExists,
    WeakPassword,
    InvalidCredentials
)
from app.models import SignupRequest, LoginRequest

app = FastAPI(title="Auth & User Management API")

@app.post("/signup")
def signup(data: SignupRequest):
    try:
        create_user(data.username, data.password)
        return {"message": "User created successfully"}
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")
    except WeakPassword:
        raise HTTPException(status_code=400, detail="Weak password")

@app.post("/login")
def login(data: LoginRequest):
    try:
        authenticate_user(data.username, data.password)
        return {"message": "Login successful"}
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid username or password")
