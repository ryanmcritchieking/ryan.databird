import json
import os
import re
import pip 
import pandas as pd
from datetime import datetime

is_admin="No"
bird_list=[]

#     defult settings

default_settings = {
    "ask_location": True,
    "when_was_it": True,
    "notes":True
}


#         files
data_file="data.json"
settings_file="setting.json"
password_file="pasword.json"




#loading jason


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









if 'birds' not in onsitedata:
    onsitedata['birds'] = []



#saving funcshon

def save_data():
    with open (data_file, 'w') as file:
        json.dump(onsitedata, file, indent=4)


def save_settings():
    with open(settings_file, 'w') as sf:
        json.dump(settings, sf, indent=4)

def save_accounts():
    with open(password_file, 'w') as file:
        json.dump(accounts_data, file, indent=4)

#      useing account

def create_account():
    username = input("Enter a new username: ").strip()
    
    
    if username.lower() == "ryan":
        for acc in accounts_data["accounts"]:
            if acc["username"].lower() == "ryan":
                print("The username 'ryan' is reserved and cannot be used.")
                return create_account()
        is_admin = True  
    else:
        is_admin = False
        for acc in accounts_data["accounts"]:
            if acc["username"].lower() == username.lower():
                print("Username already exists. Try again.")
                return create_account()

    password = input("Enter a new password: ")
    accounts_data["accounts"].append({"username": username, "password": password, "is_admin": is_admin})
    save_accounts()
    print("Account created " + ("(Admin)" if is_admin else ""))
    return username

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    for acc in accounts_data["accounts"]:
        if acc["username"] == username and acc["password"] == password:
            print(f"Welcome {username}!")
            return username
    print("Invalid username or password. Try again.")
    return login()

#login 


print("1. Login")
print("2. Create Account")
choice = input("Choose 1 or 2: ")
if choice == "1":
    current_user = login()
else:
    current_user = create_account()

#get data

if current_user not in onsitedata:
    onsitedata[current_user] = {"birds": []}


#add bird

def add_bird_data():
    type_of_bird = input("What kind of bird: ")
    bird_number = input("How many birds: ")

    # Validate number
    if not bird_number.isdigit():
        print("Invalid number, setting to 1.")
        bird_number = "1"

    where_found = ""
    if settings.get("ask_location", True):
        where_found = input("Where was it: ")

    when_was_it = ""
    if settings.get("when_was_it", True):
        when_was_it = input("When was it (or type 'd' for current date): ")
        if when_was_it.lower() == 'd':
            when_was_it = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notes = ""
    if settings.get("notes", True):
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
    print(f"The {type_of_bird} was added")



#remove all bird

def remove_all_data():
    are_you_sure = input("Are you sure you want to delete all your saved data? Type 1: ")
    if are_you_sure == "1":
        onsitedata[current_user]["birds"] = []
        save_data()
        print("Data removed.")
    else:
        print("No data removed.")



#remove bird

def remove_bird_data():
    if not onsitedata[current_user]["birds"]:
        print("No data to remove.")
        return
    removed = onsitedata[current_user]["birds"].pop()
    save_data()
    print(f"Removed: {removed}")


# show bird data

def show_bird_data():
    if not onsitedata[current_user]["birds"]:
        print("No bird data available.")
        return

    print("\nSaved Bird Data:")
    for idx, entry in enumerate(onsitedata[current_user]["birds"], start=1):
        print(f"{idx}. Bird: {entry['Bird']}, Number: {entry['Number']}, "
              f"Location: {entry['Location']}, When: {entry['When']}, Notes: {entry['Notes']}")

#export

def export_to_excel():
    if not onsitedata[current_user]["birds"]:
        print("No bird data available.")
        return

    try:
        df = pd.DataFrame(onsitedata[current_user]["birds"])
        filename = f"{current_user}_bird_data.xlsx"
        df.to_excel(filename, index=False)
        print(f"Bird data exported to {filename}")
    except Exception as e:
        print(f"Failed to export Excel file: {e}")

#open setings

def open_settings():
    while True:
        print("\nChange which questions are asked:")
        for key, value in settings.items():
            print(f"- {key}: {'ON' if value else 'OFF'}")

        print("Type the setting name to change it (e.g., ask_location), or type 'back' to return.")
        choice = input("Your choice: ").lower()

        if choice == 'back':
            break
        elif choice in settings:
            settings[choice] = not settings[choice]
            save_settings()
            print(f"{choice} set to {'ON' if settings[choice] else 'OFF'}")
        else:
            print("This is not a setting name.")



#menu

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

        elif option == '9' and is_admin:
            
        elif option == '9' and is_admin:
            
        

        else:
            print("this is not a number to choose")
            
        





show_menu()



