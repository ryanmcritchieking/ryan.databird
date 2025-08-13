import json
import os
import re
import pip
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
    were_you_find=input("were was it: ")
    when_was_it=input("when was it: ")
    line = f"{type_of_bird} | {bird_number} | {were_you_find} | {when_was_it}"
    onsitedata['birds'].append(line)   
    save_data()
    print (f"the {type_of_bird} was added")
    


def remove_all_data():
    are_you_sure=input("are you sure you want to delate all your saved data type 1: ")
    if are_you_sure=="1":

        print("data removed: ")





def remove_bird_data():
    print("nothing hear")



def show_bird_data():
    if not onsitedata['birds']:
        print("No bird data available.")
        return

    print("\nSaved Bird Data:")
    for idx, bird_entry in enumerate(onsitedata['birds'], start=1):
        type_of_bird, bird_number, where_found, when_seen = map(str.strip, bird_entry.split('|'))
        print(f"{idx}. Bird: {type_of_bird}, Number: {bird_number}, Location: {where_found}, When: {when_seen}")
    



def show_menu():
    while True:
        print('bird data saver')
        print('add bird:1')
        print('remove bird data:2')
        print('show bird data:3')
        print('export to excel')
        print('remove all5')
        print('')
        option=input("pick from 1-3: ")
        if option=='1':
            add_bird_data()
        elif option=='2':
            remove_bird_data()
        elif option=='3':
            show_bird_data()
        elif option=='4':
             print("nothing hear till update")
        elif option=='5':
            remove_all_data()
        elif option=='6':
            print("nothing hear till update")
        else:
            print("this is not a number to choose")
            
        





show_menu()