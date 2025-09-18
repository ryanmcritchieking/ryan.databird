import json
import os
import re
import pip 
import pandas as pd
from datetime import datetime

is_admin=False
bird_list=[]

# Default settings
default_settings = {
    "ask_location": True,
    "when_was_it": True,
    "notes": True
}

# Files
data_file="data.json"
settings_file="setting.json"
password_file="pasword.json"

# Loading JSON data from files if they exist
if os.path.exists(settings_file):
    with open(settings_file, 'r') as sf:
        settings = json.load(sf)
else:
    settings = default_settings.copy()

if os.path.exists(data_file):
    with open(data_file, 'r') as file:
        onsitedata = json.load(file)
else:
    onsitedata = {}

if os.path.exists(password_file):
    with open(password_file, 'r') as file:
        accounts_data = json.load(file)
else:
    accounts_data = {"accounts": []}

# Saving functions
def save_data():
    with open(data_file, 'w') as file:
        json.dump(onsitedata, file, indent=4)

def save_settings():
    with open(settings_file, 'w') as sf:
        json.dump(settings, sf, indent=4)

def save_accounts():
    with open(password_file, 'w') as file:
        json.dump(accounts_data, file, indent=4)

# Using accounts

def create_account():
    global is_admin
    # Input: New username from user
    username = input("Enter a new username: ").strip()
    
    # Admin user check for reserved username 'ryan'
    if username.lower() == "ryan":
        for acc in accounts_data["accounts"]:
            if acc["username"].lower() == "ryan":
                print("The username 'ryan' is reserved and cannot be used.")
                return create_account()
        is_admin = True  # Set as admin
    else:
        is_admin = False
        for acc in accounts_data["accounts"]:
            # Check if username already exists
            if acc["username"].lower() == username.lower():
                print("Username already exists. Try again.")
                return create_account()

    # Input: New password from user
    password = input("Enter a new password: ")
    accounts_data["accounts"].append({"username": username, "password": password, "is_admin": is_admin})
    save_accounts()
    # Output: Confirmation of account creation
    print("Account created " + ("(Admin)" if is_admin else ""))
    return username

def login():
    global is_admin
    # Input: Username from user
    username = input("Enter username: ")
    # Input: Password from user
    password = input("Enter password: ")
    for acc in accounts_data["accounts"]:
        if acc["username"] == username and acc["password"] == password:
            # Output: Welcome message on successful login
            print(f"Welcome {username}!")
            is_admin = acc.get("is_admin", False)
            return username
    # Output: Error message on failed login
    print("Invalid username or password. Try again.")
    return login()

def start():
    while True:
        # Input: User selects to login or create account
        choice = input("Type '1' to login or '2' to create a new account: ").strip().lower()
        if choice == '1':
            return login()
        elif choice == '2':
            return create_account()
        else:
            # Output: Error message for invalid input
            print("Invalid input. Please type '1' or '2'.")

current_user = start()

if current_user not in onsitedata:
    onsitedata[current_user] = {"birds": []}

# Add bird data
def add_bird_data():
    # Input: Type of bird from user
    type_of_bird = input("What kind of bird: ")
    # Input: Number of birds seen
    bird_number = input("How many birds: ")

    # Validate number input
    if not bird_number.isdigit():
        # Output: Message about invalid number input and defaulting to 1
        print("Invalid number, setting to 1.")
        bird_number = "1"

    where_found = ""
    if settings.get("ask_location", True):
        # Input: Location where bird was found (conditional)
        where_found = input("Where was it: ")

    when_was_it = ""
    if settings.get("when_was_it", True):
        # Input: Date/time of sighting or 'd' for current date (conditional)
        when_was_it = input("When was it (or type 'd' for current date): ")
        if when_was_it.lower() == 'd':
            when_was_it = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notes = ""
    if settings.get("notes", True):
        # Input: Additional notes (conditional)
        notes = input("Add notes: ")

    bird_entry = {
        "Bird": type_of_bird,
        "Number": bird_number,
        "Location": where_found,
        "When": when_was_it,
        "Notes": notes
    }

    onsitedata[current_user]["birds"].append(bird_entry)
    save_data()
    # Output: Confirmation message of bird added
    print(f"The {type_of_bird} was added")

# Remove all bird data
def remove_all_data():
    # Input: Confirm deletion by typing '1'
    are_you_sure = input("Are you sure you want to delete all your saved data? Type 1: ")
    if are_you_sure == "1":
        onsitedata[current_user]["birds"] = []
        save_data()
        # Output: Confirmation message after deletion
        print("Data removed.")
    else:
        # Output: Message when no data is removed
        print("No data removed.")

# Remove last bird entry
def remove_bird_data():
    if not onsitedata[current_user]["birds"]:
        # Output: No data available message
        print("No data to remove.")
        return
    removed = onsitedata[current_user]["birds"].pop()
    save_data()
    # Output: Confirmation showing which bird was removed
    print(f"Removed: {removed}")

# Show bird data
def show_bird_data():
    if not onsitedata[current_user]["birds"]:
        # Output: No bird data available message
        print("No bird data available.")
        return

    # Output: List all saved bird data entries for the current user
    print("\nSaved Bird Data:")
    for idx, entry in enumerate(onsitedata[current_user]["birds"], start=1):
        print(f"{idx}. Bird: {entry['Bird']}, Number: {entry['Number']}, "
              f"Location: {entry['Location']}, When: {entry['When']}, Notes: {entry['Notes']}")

# Export bird data to Excel
def export_to_excel():
    if not onsitedata[current_user]["birds"]:
        # Output: No bird data message
        print("No bird data available.")
        return

    try:
        df = pd.DataFrame(onsitedata[current_user]["birds"])
        filename = f"{current_user}_bird_data.xlsx"
        df.to_excel(filename, index=False)
        # Output: Confirmation of export with filename
        print(f"Bird data exported to {filename}")
    except Exception as e:
        # Output: Error message if export fails
        print(f"Failed to export Excel file: {e}")

# Open settings menu to toggle questions
def open_settings():
    while True:
        print("\nChange which questions are asked:")
        for key, value in settings.items():
            # Output: Show each setting and whether it's ON or OFF
            print(f"- {key}: {'ON' if value else 'OFF'}")

        # Input: Ask user which setting to change or to return
        print("Type the setting name to change it (e.g., ask_location), or type 'back' to return.")
        choice = input("Your choice: ").lower()

        if choice == 'back':
            break
        elif choice in settings:
            settings[choice] = not settings[choice]
            save_settings()
            # Output: Confirmation of changed setting status
            print(f"{choice} set to {'ON' if settings[choice] else 'OFF'}")
        else:
            # Output: Invalid setting name message
            print("This is not a setting name.")

# Show all users' bird data (admin only)
def show_all_data():
    # Output: Header for all users' bird data
    print("\nAll users bird data:")
    for user, data in onsitedata.items():
        print(f"\nUser: {user}")
        if not isinstance(data, dict):
            print("  Invalid data format for this user.")
            continue
        birds = data.get("birds", [])
        if not birds:
            print("  No bird data.")
            continue
        # Output: List bird data per user
        for idx, entry in enumerate(birds, start=1):
            print(f"  {idx}. Bird: {entry['Bird']}, Number: {entry['Number']}, "
                  f"Location: {entry['Location']}, When: {entry['When']}, Notes: {entry['Notes']}")

# Show all account usernames and passwords (admin only)
def show_all_passwords():
    print("\nAll accounts:")
    for acc in accounts_data.get("accounts", []):
        # Output: Show username, password, and admin status
        print(f"Username: {acc['username']}, Password: {acc['password']}, Admin: {acc.get('is_admin', False)}")

# Remove accounts (admin only)
def remove_accounts():
    print("\nAll accounts:")
    for i, acc in enumerate(accounts_data.get("accounts", []), start=1):
        print(f"{i}. {acc['username']} (Admin: {acc.get('is_admin', False)})")

    # Input: Ask which account to remove or cancel
    username_to_remove = input("Enter the username to remove (or 'back' to cancel): ").strip()
    if username_to_remove.lower() == 'back':
        return

    for acc in accounts_data["accounts"]:
        if acc["username"].lower() == username_to_remove.lower():
            if acc.get("is_admin", False):
                # Output: Cannot remove admin message
                print("You cannot remove an admin account.")
                return
            accounts_data["accounts"].remove(acc)
            # Remove associated bird data if any
            if username_to_remove in onsitedata:
                del onsitedata[username_to_remove]
            save_accounts()
            save_data()
            # Output: Confirmation of removal
            print(f"Account '{username_to_remove}' and their data have been removed.")
            return
    # Output: No account found message
    print(f"No account found with username '{username_to_remove}'.")

# Main menu for user actions
def show_menu():
    while True:
        print('bird data saver ')
        print('')
        print('1. add bird: ')
        print('2. remove bird data: ')
        print('3.show bird data: ')
        print('4.export to excel: ')
        print('5.remove all: ')
        print('6.settings: ')
        print('7.logout or exit: ')
        if is_admin:
            print('8. ADMIN: view all users bird data: ')
        if is_admin:
            print('9. ADMIN: view all uses and paswrod: ')
        if is_admin:
            print('10. ADMIN: remove acounts: ')
        # Input: User selects an option
        option=input("pick from 1-7: ")
        if option=='1':
            add_bird_data()
        elif option=='2':
            remove_bird_data()
        elif option=='3':
            show_bird_data()
        elif option=='4':
            export_to_excel()
        elif option=='5':
            remove_all_data()
        elif option=='6':
            open_settings()
        elif option=='7':
            break
        elif option == '8' and is_admin:
            show_all_data()
        elif option == '9' and is_admin:
            show_all_passwords()
        elif option == '10' and is_admin:
            remove_accounts()
        else:
            # Output: Invalid menu option message
            print("this is not a number to choose")

show_menu()