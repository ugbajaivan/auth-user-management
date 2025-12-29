import requests
from datetime import datetime

# FIRST, you need to login to get a new token
print("Getting a NEW token...")
login_response = requests.post(
    "http://127.0.0.1:8000/login",
    json={"username": "billy", "password": "YOUR_PASSWORD_HERE"}  # Use the password you created for billy
)

if login_response.status_code == 200:
    new_token = login_response.json()["access_token"]
    print(f"Got NEW token: {new_token[:50]}...")
    
    # Test with new token
    response = requests.get(
        "http://127.0.0.1:8000/protected",
        headers={"Authorization": f"Bearer {new_token}"}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text}")
else:
    print(f"Login failed: {login_response.text}")
    print("\nCreate a NEW user instead:")
    
    # Create new user if you don't remember billy's password
    signup_response = requests.post(
        "http://127.0.0.1:8000/signup",
        json={"username": "testuser", "password": "Test123!"}
    )
    print(f"Signup: {signup_response.json()}")