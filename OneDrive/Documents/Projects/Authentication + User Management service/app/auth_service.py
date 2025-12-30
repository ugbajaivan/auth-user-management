import bcrypt
import jwt
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session
from .database import User

logger = logging.getLogger(__name__)

# ============================================
# JWT CONFIGURATION
# ============================================
SECRET_KEY = "my-super-secure-jwt-secret-key-12345!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

print("=" * 50)
print("AUTH SERVICE INITIALIZED")
print(f"SECRET_KEY: {SECRET_KEY[:15]}...")
print(f"ALGORITHM: {ALGORITHM}")
print(f"EXPIRY: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
print("=" * 50)

# Exception classes
class AuthError(Exception): pass
class UserAlreadyExists(AuthError): pass
class WeakPassword(AuthError): pass
class InvalidCredentials(AuthError): pass

# Password validation
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


# ============================================
# DATABASE OPERATIONS
# ============================================
def create_user(db: Session, username: str, password: str):
    """
    Create new user in DATABASE
    """
    logger.info(f"Creating user: {username}")
    
    if not password_valid(password):
        raise WeakPassword("Password too weak")
    
    # Check if user exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise UserAlreadyExists("User already exists")
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # Create User object
    new_user = User(username=username, password_hash=password_hash)
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User created with ID: {new_user.id}")
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate user from DATABASE
    """
    logger.info(f"Authenticating user: {username}")
    
    # Find user
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise InvalidCredentials("User not found")
    
    # Verify password
    if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        logger.info(f"Authentication successful for: {username}")
        return True
    else:
        raise InvalidCredentials("Invalid password")


# ============================================
# JWT FUNCTIONS
# ============================================
def create_access_token(data: dict):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    logger.info(f"Creating token with payload: {to_encode}")
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token created: {token[:30]}...")
    
    return token


def decode_access_token(token: str):
    """Decode JWT token"""
    logger.info(f"Attempting to decode token")
    
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