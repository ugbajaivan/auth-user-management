from auth_service import (
    create_user,
    authenticate_user,
    UserAlreadyExists,
    WeakPassword,
    InvalidCredentials
)

try:
    create_user("ivan", "Strong@123")
    print("User created")
except UserAlreadyExists:
    print("User already exists")
except WeakPassword:
    print("Weak password")

try:
    authenticate_user("ivan", "Strong@123")
    print("Login success")
except InvalidCredentials:
    print("Login failed")