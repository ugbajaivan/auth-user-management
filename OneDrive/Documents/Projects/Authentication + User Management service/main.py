from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, HTTPException, Depends, Request
from app.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    decode_access_token,
    UserAlreadyExists,
    WeakPassword,
    InvalidCredentials,
    SECRET_KEY,  # Import directly to verify
    ALGORITHM    # Import directly to verify
)
from app.models import SignupRequest, LoginRequest
import logging

# ============================================
# SETUP LOGGING - This is CRUCIAL for debugging
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Auth & User Management API - Learning Edition",
    description="A complete authentication system with JWT tokens. Built for learning!",
    version="1.0.0"
)

security = HTTPBearer()

# ============================================
# MIDDLEWARE FOR LOGGING ALL REQUESTS
# ============================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"Request: {request.method} {request.url}")
    
    # Check for Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header:
        logger.info(f"Auth header present: {auth_header[:30]}...")
    
    response = await call_next(request)
    return response

# ============================================
# API ENDPOINTS
# ============================================
@app.post("/signup")
def signup(data: SignupRequest):
    """
    Create a new user account
    
    Requirements:
    - Username must be unique
    - Password must contain: uppercase, lowercase, number, and special character
    - Minimum 6 characters
    
    Example password: "Test123!"
    """
    logger.info(f"Signup attempt for username: {data.username}")
    
    try:
        create_user(data.username, data.password)
        logger.info(f"User created successfully: {data.username}")
        return {
            "message": "User created successfully",
            "username": data.username,
            "next_step": "Use /login to get a JWT token"
        }
    except UserAlreadyExists:
        logger.warning(f"User already exists: {data.username}")
        raise HTTPException(status_code=409, detail="User already exists")
    except WeakPassword:
        logger.warning(f"Weak password for: {data.username}")
        raise HTTPException(
            status_code=400, 
            detail="Weak password. Must contain: uppercase, lowercase, number, special character (!.@#$%^&*()_[]), and be at least 6 characters"
        )

@app.post("/login")
def login(data: LoginRequest):
    """
    Authenticate and receive a JWT token
    
    Returns:
    - access_token: JWT token to use in Authorization header
    - token_type: Always "bearer"
    
    How to use the token:
    Add to request headers: "Authorization: Bearer YOUR_TOKEN_HERE"
    """
    logger.info(f"Login attempt for username: {data.username}")
    
    try:
        # Step 1: Verify credentials
        authenticate_user(data.username, data.password)
        logger.info(f"Credentials valid for: {data.username}")
        
        # Step 2: Create JWT token
        token = create_access_token({"sub": data.username})
        
        # Log token info (safely)
        token_preview = token[:50] + "..." if len(token) > 50 else token
        logger.info(f"Token created for {data.username}: {token_preview}")
        logger.info(f"Token will expire in 30 minutes")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "instructions": "Use this token in the Authorization header: 'Bearer YOUR_TOKEN'",
            "test_endpoint": "/test-token-debug (POST your token here to verify)"
        }
    except InvalidCredentials:
        logger.warning(f"Invalid credentials for: {data.username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

# ============================================
# TOKEN VERIFICATION & PROTECTED ROUTES
# ============================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Dependency function to extract and verify JWT token
    
    This function:
    1. Extracts token from "Bearer TOKEN" header
    2. Decodes and verifies the token
    3. Returns the username from token payload
    
    If token is invalid/expired, returns 401 Unauthorized
    """
    
    token = credentials.credentials
    
    # Fix common user errors
    # Remove extra "Bearer " if user typed it
    if token.startswith("Bearer "):
        token = token[7:]  # Remove "Bearer "
        logger.warning("User included 'Bearer' in token, removing it...")
    
    logger.info(f"Token verification requested")
    logger.info(f"Token received: {token[:30]}...")
    
    try:
        payload = decode_access_token(token)
        username = payload["sub"]
        logger.info(f"Token valid! User authenticated: {username}")
        return username
    except Exception as e:
        logger.error(f"Token verification FAILED: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    """
    Example protected endpoint
    
    Requires valid JWT token in Authorization header
    
    Try it: 
    1. Get token from /login
    2. Click "Authorize" button (top-right in docs)
    3. Enter: "Bearer YOUR_TOKEN"
    4. Try this endpoint
    """
    return {
        "message": f"Hello {current_user}!",
        "note": "You successfully accessed a protected route",
        "user": current_user,
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# DEBUG & LEARNING ENDPOINTS
# ============================================
from datetime import datetime, timedelta

@app.get("/")
def root():
    """Welcome endpoint with API information"""
    return {
        "api": "Authentication & User Management Service",
        "version": "1.0.0",
        "author": "Your Name Here",
        "endpoints": {
            "signup": "/signup (POST)",
            "login": "/login (POST)",
            "protected": "/protected (GET - requires auth)",
            "verify": "/verify-config (GET)",
            "test": "/test-jwt-direct (GET)"
        },
        "github": "Add your GitHub repo URL here"
    }

@app.get("/verify-config")
def verify_jwt_config():
    """Verify JWT configuration is consistent"""
    from app.auth_service import SECRET_KEY, ALGORITHM
    
    return {
        "jwt_configuration": {
            "secret_key_length": len(SECRET_KEY),
            "secret_key_preview": SECRET_KEY[:15] + "...",
            "algorithm": ALGORITHM,
            "token_expiry_minutes": 30
        },
        "verification": {
            "same_key_for_encode_decode": True,
            "note": "If encoding and decoding use different keys, tokens won't verify"
        }
    }

@app.post("/test-token-debug")
def debug_token_test(token: str):
    """
    Debug endpoint to test token decoding
    
    Paste your token here to see if it decodes correctly
    Useful for troubleshooting
    """
    logger.info(f"Debug token test received token: {token[:50]}...")
    
    try:
        payload = decode_access_token(token)
        return {
            "success": True,
            "message": "Token is valid!",
            "decoded_payload": payload,
            "user": payload.get("sub"),
            "expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat() if payload.get("exp") else None,
            "token_preview": token[:50] + "..."
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Token is INVALID",
            "error": str(e),
            "error_type": type(e).__name__,
            "token_received": token[:100] + "..." if len(token) > 100 else token,
            "troubleshooting": [
                "Check if SECRET_KEY is the same in auth_service.py",
                "Make sure token hasn't expired (30 minutes)",
                "Verify no extra spaces in token",
                "Try creating a new token with /login"
            ]
        }

@app.get("/test-jwt-direct")
def test_jwt_direct_creation():
    """Direct JWT test bypassing the auth service"""
    from app.auth_service import SECRET_KEY, ALGORITHM
    import jwt
    
    # Create a simple test token
    test_payload = {
        "sub": "testuser",
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "test": True
    }
    
    token = jwt.encode(test_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    # Try to decode it
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "test": "Direct JWT encode/decode test",
            "status": "SUCCESS",
            "token_created": token,
            "token_decoded": decoded,
            "config_used": {
                "secret_key": SECRET_KEY[:10] + "...",
                "algorithm": ALGORITHM
            }
        }
    except Exception as e:
        return {
            "test": "Direct JWT encode/decode test",
            "status": "FAILED",
            "error": str(e),
            "config_used": {
                "secret_key": SECRET_KEY[:10] + "...",
                "algorithm": ALGORITHM
            }
        }

# ============================================
# USER MANAGEMENT ENDPOINTS (For learning)
# ============================================
@app.get("/users/count")
def count_users():
    """Count how many users are registered (for learning)"""
    import os
    filename = "users.csv"
    
    if not os.path.exists(filename):
        return {"total_users": 0, "file_exists": False}
    
    with open(filename, 'r') as file:
        # Subtract 1 for header row
        total = sum(1 for line in file) - 1
    
    return {
        "total_users": max(total, 0),
        "file_exists": True,
        "filename": filename
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)