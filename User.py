import sqlite3 as sql
import random
import os
import json
import io
import datetime as dt

db = sql.connect('Databases\\User Database.db')           # Connecting to Database
cursor = db.cursor()                                  # Making Cursor

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        Username TEXT PRIMARY KEY, 
        Password TEXT, 
        Email TEXT, 
        Phone TEXT, 
        DOB DATE, 
        ProfilePic BLOB, 
        Bio TEXT,
        Recoverykey TEXT
    )
''')

cursor.close()          # Closing cursor
db.close()              # Closing Database

def sign_up(usr, pas, email, phone, dob, profile_pic, bio):
    if usr and pas and len(pas) >= 8:
        db = sql.connect('Databases\\User Database.db')
        cursor = db.cursor()
        
        try:
            profile_pic_data = profile_pic.read() if profile_pic else None
            key = generate_recovery_key()
            cursor.execute('''
                INSERT INTO users (Username, Password, Email, Phone, DOB, ProfilePic, Bio, Recoverykey) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (usr, pas, email, phone, dob, profile_pic_data, bio, key))
            
            db.commit()
            cursor.close()
            db.close()
            
            path = os.path.join('Users', usr)
            if not os.path.exists(path):
                os.makedirs(path)

            return f"Account Created Successfully. Your recovery key is: {key}"
        except sql.IntegrityError:
            cursor.close()
            db.close()
            return "Account Creation Failed. Username already exists."
    else:
        return "Invalid input."

def generate_recovery_key():
    """Generate a random recovery key of 10 characters (letters and digits)."""
    characters = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789'
    return ''.join(random.choice(characters) for _ in range(10))

def sign_in(usr,pas):
    db = sql.connect('Databases\\User Database.db')           # Connecting to Database
    cursor = db.cursor()                                  # Making Cursor

    cursor.execute("SELECT * FROM users WHERE username=?AND password=?",(usr,pas))
    result = cursor.fetchone()

    cursor.close()          # Closing cursor
    db.close()              # Closing Database

    if result:
        return True

def fetch_user_details(username):
    db = sql.connect('Databases\\User Database.db')
    cursor = db.cursor()
    
    cursor.execute("SELECT Username, Email, Phone, DOB, ProfilePic, Bio FROM users WHERE Username = ?", (username,))
    result = cursor.fetchone()
    
    cursor.close()
    db.close()

    if result:
        return {
            "username": result[0],
            "email": result[1],
            "phone": result[2],
            "dob": result[3],
            "profile_pic": result[4],
            "bio": result[5],
        }
    else:
        return None

def delete_acc(usr,pas):
    db = sql.connect('Databases\\User Database.db')           # Connecting to Database
    cursor = db.cursor()                                  # Making Cursor

    cursor.execute("DELETE FROM users WHERE username=? AND password=?",(usr,pas))

    if cursor.rowcount == 0:
        cursor.close()          # Closing cursor
        db.close()              # Closing Database
        return ("Deletion Failed", "Invalid username or password")
    else:
        log("Account Deletion", usr)
        db.commit()
        cursor.close()          # Closing cursor
        db.close()              # Closing Database
        return ("Account Deleted", "Your account has been deleted successfully!") 
    
def change_pas(usr,oldpas,newpas):
    db = sql.connect('Databases\\User Database.db')           # Connecting to Database
    cursor = db.cursor()                                  # Making Cursor 

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (usr, oldpas))          
    result = cursor.fetchone()
    
    if result:
        cursor.execute("UPDATE users SET password=? WHERE username=?", (newpas, usr))             # Updates password
        db.commit()
        cursor.close()          # Closing cursor
        db.close()              # Closing Database
        log("Password Change", usr)
        return ("Password Changed", "Your password has been changed successfully!")

    else:
        cursor.close()          # Closing cursor
        db.close()              # Closing Database
        return ("Change Password Failed", "Invalid username or old password")
 
def reset_pas(usr,key,npas):
    db = sql.connect('Databases\\User Database.db')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT Recoverykey FROM users WHERE Username = ?", (usr,))
        stored_key = cursor.fetchone()

        if stored_key or stored_key[0] == key:
            cursor.execute("UPDATE users SET Password = ? WHERE Username = ?", (npas, usr))
            db.commit()
            log("Password Reset", usr)
            return "Password reset successful"
        else:
            return "Invalid recovery key"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        db.close()

def log(action, username, details=None):
    timestamp = dt.datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "username": username,
        "action": action
    }
    if details:
        log_entry["details"] = details
    
    log_file_path = "Databases\\activity_log.json"
    
    try:
        with open(log_file_path, 'r') as log_file:
            log_data = json.load(log_file)
    except:
        log_data = []
    
    log_data.append(log_entry)
    
    with open(log_file_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=2)

def update_profile(username, email, phone, dob, profile_pic, bio):
    conn = sql.connect('Databases\\User Database.db')
    c = conn.cursor()
    
    # Convert the profile picture to binary format
    if profile_pic is not None:
        profile_pic_data = profile_pic.read()
    dob_str = dob.strftime('%Y-%m-%d') if dob else None

    if profile_pic_data:
        c.execute('''
            UPDATE users 
            SET Email = ?, Phone = ?, DOB = ?, ProfilePic = ?, Bio = ?
            WHERE Username = ?''', 
            (email, phone, dob_str, profile_pic_data, bio, username))
    else:
        c.execute('''
            UPDATE users 
            SET Email = ?, Phone = ?, DOB = ?, Bio = ?
            WHERE Username = ?''', 
            (email, phone, dob_str, bio, username))
    
    conn.commit()
    c.close()
    conn.close()

def get_email(username):
    db = sql.connect('Databases\\User Database.db')           # Connecting to Database
    cursor = db.cursor()    

    cursor.execute("SELECT Email FROM users WHERE Username = ?", (username,))
    result = cursor.fetchone()

    cursor.close()          # Closing cursor
    db.close()              # Closing Database

    return result