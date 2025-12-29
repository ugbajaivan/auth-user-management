import bcrypt
import csv
import os
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# ============================================
# CRITICAL: SINGLE SOURCE OF TRUTH FOR JWT CONFIG
# ============================================
SECRET_KEY = "my-super-secure-jwt-secret-key-12345!"  # Must be the same everywhere
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

print("=" * 50)
print("AUTH SERVICE INITIALIZED")
print(f"SECRET_KEY: {SECRET_KEY[:15]}...")
print(f"ALGORITHM: {ALGORITHM}")
print(f"EXPIRY: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
print("=" * 50)

# Exception classes (keep these)
class AuthError(Exception): pass
class UserAlreadyExists(AuthError): pass
class WeakPassword(AuthError): pass
class InvalidCredentials(AuthError): pass

# Password validation (keep this)
LEGAL_SYMBOLS = "!.@#$%^&*()_[]"

def password_valid(password: str) -> bool:
    """Check password strength"""
    if len(password) < 6:
        return False
    
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(ch in LEGAL_SYMBOLS for ch in password)

    return all([has_upper, has_lower, has_digit, has_symbol])

def create_user(userid: str, password: str, filename="users.csv"):
    """Create new user"""
    if not password_valid(password):
        raise WeakPassword("Password too weak")
    
    # Check existing users
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[0]:
                    existing.add(row[0])
    
    if userid in existing:
        raise UserAlreadyExists("User exists")
    
    # Hash and save
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            writer.writerow(["userid", "password_hash"])
        writer.writerow([userid, hashed])
    
    logger.info(f"User created: {userid}")

def authenticate_user(userid: str, password: str, filename="users.csv"):
    """Authenticate user"""
    if not os.path.exists(filename):
        raise InvalidCredentials("Invalid credentials")
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[0] == userid:
                if bcrypt.checkpw(password.encode(), row[1].encode()):
                    return True
                else:
                    raise InvalidCredentials("Invalid credentials")
    
    raise InvalidCredentials("Invalid credentials")

# ============================================
# JWT FUNCTIONS - SIMPLIFIED FOR DEBUGGING
# ============================================
def create_access_token(data: dict):
    """Create JWT token - SIMPLIFIED VERSION"""
    to_encode = data.copy()
    
    # Add expiration
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    logger.info(f"Creating token with payload: {to_encode}")
    logger.info(f"Using SECRET_KEY: {SECRET_KEY[:10]}...")
    
    # Create token
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    logger.info(f"Token created (first 30 chars): {token[:30]}...")
    logger.info(f"Full token length: {len(token)} characters")
    
    return token

def decode_access_token(token: str):
    """Decode JWT token - SIMPLIFIED VERSION"""
    logger.info(f"Attempting to decode token")
    logger.info(f"Token input: {token[:30]}...")
    logger.info(f"Using SECRET_KEY: {SECRET_KEY[:10]}...")
    logger.info(f"Using ALGORITHM: {ALGORITHM}")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decode SUCCESS! User: {payload.get('sub')}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token expired")
        raise InvalidCredentials("Token expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise InvalidCredentials(f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        raise InvalidCredentials(f"Token error: {str(e)}")