import json
import os
import re

data="data.json"

if os.path.exists(data):
    with open(data, 'r') as file:
        onsitedata = json.load(file)
else:
    onsitedata = {}


def save_data():
    with open (data, 'w') as file:
        json.dump(onsitedata, file, indent=4)



def add_bird_data():
    type_of_bird=input("what kind of bird: ")
    bird_number=input("how many bird: ")
    were_you_find=input("were was it: ")
    when_was_it=input("when was it: ")



def add_lots_bird_data():
    print("nothing hear")



def remove_bird_data():
    print("nothing hear")



def show_bird_data():
    print("nothing hear")



def show_menu():
    while True:
        print('bird data saver')
        print('add bird:1')
        print('add more than onebird:2')
        print('remove bird data:3')
        print('show bird data:4')
        option=input("pick from 1-4: ")
        if option=='1':
            add_bird_data()
        elif option=='2':
            add_lots_bird_data()
        elif option=='3':
            remove_bird_data()
        elif option=='4':
            show_bird_data()
        elif option=='5':
            print("nothing hear to update")
        elif option=='6':
            print("nothing hear to update")
        else:
            print("this is not a number to choose")
            
        





show_menu()