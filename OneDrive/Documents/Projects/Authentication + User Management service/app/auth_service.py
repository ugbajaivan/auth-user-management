class AuthError(Exception):
    """Raised for authentication related errors"""
    pass

class UserAlreadyExists(AuthError):
    """Raised when attempting to create a user that already exists"""
    pass

class WeakPassword(AuthError):
    """Raised when a password does not meet security requirements"""
    pass

class InvalidCredentials(AuthError):
    """Raised when provided credentials are invalid"""
    pass

import bcrypt
import csv
import os

LEGAL_SYMBOLS = "!.@#$%^&*()_[]"

def password_valid(password: str) -> bool:
    """
    Checks if a password meets strength requirements

    Args:
        password (str): Password being checked

    Returns:
        bool: Returns true or false based on whether password meets requirements
    """
    
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(ch in LEGAL_SYMBOLS for ch in password)

    return (
        len(password) >= 6
        and has_upper
        and has_lower
        and has_digit
        and has_symbol
    )

def create_user(userid: str, password: str, filename="users.csv"):
    if not password_valid(password):
        raise WeakPassword("Password does not meet security requirements")

    existing_users = set()

    if os.path.exists(filename):
        with open(filename, newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    existing_users.add(row[0])

    if userid in existing_users:
        raise UserAlreadyExists("Username already exists")

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["userid", "password_hash"])
        writer.writerow([userid, hashed])


def authenticate_user(userid: str, password: str, filename="users.csv") -> bool:
    if not os.path.exists(filename):
        raise InvalidCredentials("Invalid username or password")

    with open(filename, newline="") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            stored_user, stored_hash = row

            if stored_user == userid:
                if bcrypt.checkpw(
                    password.encode("utf-8"),
                    stored_hash.encode("utf-8")
                ):
                    return True
                else:
                    raise InvalidCredentials("Invalid username or password")

    raise InvalidCredentials("Invalid username or password")


if __name__ == "__main__":
    print(password_valid("WeakPass"))  # Expected: False
    print(password_valid("Strong@123"))  # Expected: True