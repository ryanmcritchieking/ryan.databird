import json
import os
import re
import pip 
import pandas as pd
from datetime import datetime


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
    username = input("Enter a new username: ")
    for acc in accounts_data["accounts"]:
        if acc["username"] == username:
            print("Username already exists. Try again.")
            return create_account()
    password = input("Enter a new password: ")
    accounts_data["accounts"].append({"username": username, "password": password})
    save_accounts()
    print("Account created ")
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






def add_bird_data():
    type_of_bird=input("what kind of bird: ")
    bird_number=input("how many birds: ")
   
   
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
        notes = input("add notes: ")


    
    line = f"{type_of_bird} | {bird_number} | {where_found} | {when_was_it} | {notes}"
    onsitedata['birds'].append(line)   
    save_data()
    print (f"the {type_of_bird} was added")
    


def remove_all_data():
    are_you_sure=input("are you sure you want to delate all your saved data type 1: ")
    if are_you_sure=="1":
        onsitedata["birds"]=[]
        save_data()
        print("data removed: ")
    else:
        print("no data removed")





def remove_bird_data():
    if not onsitedata["birds"]:
        print("no data to remove")
        return
    removed=onsitedata["birds"].pop()
    save_data()
    print(f"removed{removed}")




def show_bird_data():
    if not onsitedata['birds']:
        print("No bird data available.")
        return

    print("\nSaved Bird Data:")
    for idx, entry in enumerate(onsitedata['birds'], start=1):
        parts = list(map(str.strip, entry.split('|')))
        while len(parts) < 5:
            parts.append("")  
        type_of_bird, bird_number, where_found, when_seen, notes = parts
        print(f"{idx}. Bird: {type_of_bird}, Number: {bird_number}, Location: {where_found}, When: {when_seen}, Notes: {notes}")
    



def export_to_excel():
    if not onsitedata["birds"]:
        print("No bird data available.")
        return

    bird_list = []  

    for entry in onsitedata["birds"]:
        parts = list(map(str.strip, entry.split('|')))
        while len(parts) < 5:
            parts.append("") 
        type_of_bird, bird_number, where_found, when_seen, notes = parts
        bird_list.append({
            'Bird': type_of_bird,
            'Number': bird_number,
            'Location': where_found,
            'When': when_seen,
            'Notes': notes
        })


    try:
        df = pd.DataFrame(bird_list)
        df.to_excel("bird_data.xlsx", index=False)
        print("bird data exported to bird_data.xlsx")
    except Exception as e:
        print(f"failed to export Excel file: {e}")



def open_settings():
    while True:
        print("chade wich quesgens are asked: ")
        for key, value in settings.items():
            print(f"- {key}: {'ON' if value else 'OFF'}")
        
        print("put the setting name to change it like ask_location or when_was_it if not type back to return.")
        choice = input("Your choice: ").lower()

        if choice == 'back':
            break
        elif choice in settings:
            settings[choice] = not settings[choice]
            save_settings()
            print(f"{choice} set to {'ON' if settings[choice] else 'OFF'}")
        else:
            print("this not setting name.")



def show_menu():
    while True:
        print('bird data saver ')
        print('add bird:1 ')
        print('remove bird data:2 ')
        print('show bird data:3 ')
        print('export to excel:4 ')
        print('remove all:5 ')
        print('settings:6 ')
        option=input("pick from 1-6: ")
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
        else:
            print("this is not a number to choose")
            
        





show_menu()



