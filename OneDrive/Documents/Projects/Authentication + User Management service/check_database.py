# check_db_simple.py
import sqlite3
import os

print("="*60)
print("DATABASE DIAGNOSTIC TOOL")
print("="*60)

# Check if database file exists
db_file = "users.db"
print(f"1. Checking for database file: {db_file}")

if os.path.exists(db_file):
    file_size = os.path.getsize(db_file)
    print(f"   ✅ File exists ({file_size} bytes)")
    
    # Try to connect
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print("   ✅ Connected to database successfully")
        
        # Check if 'users' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n2. Tables in database:")
        if tables:
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("   ❌ No tables found!")
            
        # Check 'users' table specifically
        print(f"\n3. Checking 'users' table:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        users_table = cursor.fetchone()
        
        if users_table:
            print("   ✅ 'users' table exists")
            
            # Count users
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   Total users: {user_count}")
            
            # List all users
            if user_count > 0:
                cursor.execute("SELECT id, username FROM users")
                users = cursor.fetchall()
                print("\n4. Registered users:")
                for user in users:
                    print(f"   ID: {user[0]}, Username: {user[1]}")
            else:
                print("\n4. ❌ No users in the database!")
                
            # Show table structure
            print(f"\n5. Table structure:")
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   Column: {col[1]} (Type: {col[2]})")
                
        else:
            print("   ❌ 'users' table does not exist!")
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"   ❌ Database error: {e}")
        
else:
    print(f"   ❌ Database file NOT found!")
    print("\nCreating a new database...")
    
    # Create a simple database
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create users table (matching your app structure)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("   ✅ Created new users.db with 'users' table")
        
    except Exception as e:
        print(f"   ❌ Failed to create database: {e}")

print("\n" + "="*60)
print("RECOMMENDED ACTIONS:")
print("="*60)

if os.path.exists(db_file):
    print("1. If no users exist, create one via API or manually")
    print("2. If database looks empty, you might need to run your app's init")
else:
    print("1. Start your FastAPI app to initialize the database")
    print("2. Or run: python -c \"from app.database import create_tables; create_tables()\"")

print("\nQuick test command:")
print('python -c "import sqlite3; conn=sqlite3.connect(\"users.db\"); c=conn.cursor(); c.execute(\"SELECT * FROM users\"); print(c.fetchall()); conn.close()"')