import hashlib
import json
import os

def create_and_store_password():
    """
    Ask user for username and password, encrypt the password using SHA-256,
    and store it in passwords.json file.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Encrypt password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Initialize empty dict if file doesn't exist or load existing data
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            try:
                passwords_dict = json.load(file)
            except json.JSONDecodeError:
                passwords_dict = {}
    else:
        passwords_dict = {}
    
    # Store username and hashed password
    passwords_dict[username] = hashed_password
    
    # Write back to file
    with open("passwords.json", "w") as file:
        json.dump(passwords_dict, file, indent=4)
    
    print(f"Password for {username} has been stored successfully!")

def fetch_and_check_password():
    """
    Ask user for username and password, verify if the password matches
    the stored hashed password for that username.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Hash the input password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Check if passwords.json exists
    if not os.path.exists("passwords.json"):
        print("No passwords have been stored yet.")
        return
    
    # Load passwords from file
    with open("passwords.json", "r") as file:
        try:
            passwords_dict = json.load(file)
        except json.JSONDecodeError:
            print("Password file is corrupted or empty.")
            return
    
    # Check if username exists and password matches
    if username in passwords_dict:
        if passwords_dict[username] == hashed_password:
            print("Verified! Password is correct.")
        else:
            print("Password is incorrect.")
    else:
        print(f"Username '{username}' not found.")

# Example usage:
if __name__ == "__main__":
    print("1. Create and store a password")
    print("2. Verify a password")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        create_and_store_password()
    elif choice == "2":
        fetch_and_check_password()
    else:
        print("Invalid choice!")
