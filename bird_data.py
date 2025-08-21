import json
import os
import re
import pip 
import pandas as pd
from datetime import datetime


bird_list=[]

settings = {
    "ask_location": True,
    "when_was_it": True
}



data_file="data.json"

if os.path.exists(data_file):
    with open(data_file, 'r') as file:
        onsitedata = json.load(file)
else:
    onsitedata = {}



if 'birds' not in onsitedata:
    onsitedata['birds'] = []


def save_data():
    with open (data_file, 'w') as file:
        json.dump(onsitedata, file, indent=4)




def add_bird_data():
    type_of_bird=input("what kind of bird: ")
    bird_number=input("how many birds: ")
   
   
    where_found = ""
    if settings.get("ask_location", True):
        where_found = input("Where was it: ")


    when_was_it = ""
    if settings.get("ask_when", True):
        when_was_it = input("When was it (or type 'd' for current date): ")
        if when_was_it.lower() == 'd':
            when_was_it = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    line = f"{type_of_bird} | {bird_number} | {where_found} | {when_was_it}"
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
    for idx, bird_entry in enumerate(onsitedata['birds'], start=1):
        type_of_bird, bird_number, where_found, when_seen = map(str.strip, bird_entry.split('|'))
        print(f"{idx}. Bird: {type_of_bird}, Number: {bird_number}, Location: {where_found}, When: {when_seen}")
    

def export_to_excel():
    if not onsitedata["birds"]:
         print("No bird data available.")
         return

    
    for entry in onsitedata["birds"]:
        type_of_bird, bird_number, where_found, when_seen = map(str.strip, entry.split('|'))
        bird_list.append({
            'Bird': type_of_bird,
            'Number': bird_number,
            'Location': where_found,
            'When': when_seen
        })
    df = pd.DataFrame(bird_list)
    df.to_excel("bird_data.xlsx", index=False)
    print("Bird data sent to bird_data.xlsx")



def open_settings():
    print ("not done yet")



def show_menu():
    while True:
        print('bird data saver ')
        print('add bird:1 ')
        print('remove bird data:2 ')
        print('show bird data:3 ')
        print('export to excel:4 ')
        print('remove all:5 ')
        print('settings:6 ')
        option=input("pick from 1-5: ")
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