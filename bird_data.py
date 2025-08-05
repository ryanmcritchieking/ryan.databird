import json
import os
import re

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
    







def remove_bird_data():
    print("nothing hear")



def show_bird_data():
    print("nothing hear")



def show_menu():
    while True:
        print('bird data saver')
        print('add bird:1')
        print('remove bird data:2')
        print('show bird data:3')
        print('')
        print('')
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
            print("nothing hear till update")
        elif option=='6':
            print("nothing hear till update")
        else:
            print("this is not a number to choose")
            
        





show_menu()