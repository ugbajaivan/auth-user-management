from app.database import create_tables, SessionLocal, User

print("Testing database creation...")

# 1. Create tables
create_tables()

# 2. Check if we can connect
db = SessionLocal()
try:
    # Count users
    user_count = db.query(User).count()
    print(f"✅ Database working! User count: {user_count}")
    
    # Try to insert a test user
    from app.auth_service import create_user
    create_user(db, "testuser", "Test123!")
    print("✅ Test user created!")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()

print("Check if users.db file exists now...")