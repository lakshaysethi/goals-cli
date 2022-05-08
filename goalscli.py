import os
import sys
import datetime
import json
from time import sleep

from typing import Mapping,Dict
from tinydb import TinyDB, Query


newzealnd = 12
database = TinyDB('cli.json')
main_goals_array = database.all()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_to_database():
    database.truncate()
    for goal in main_goals_array:
        database.insert(goal)

def getNow():
    return datetime.datetime.utcnow()+ datetime.timedelta(hours=newzealnd)
class Goal(Dict):
    def __init__(self,name):
        self["name"] = name
        self["subgoals"] = []
        self["done"] = False
        # self["created"] = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
        self["created"] = datetime.datetime.now().timestamp()
       

def toggle_hide(array_of_goals):
    clear_screen()
    selected_goal =  get_user_to_select_a_goal(array_of_goals,verb="hide/unhide")
    if selected_goal==None: 
        print("not found")
        return 
    selected_goal["done"] = not selected_goal["done"]
    save_to_database()
    clear_screen()
    print("Changed")
    return

def print_all_goals(goals_array,hide=False):
    for index,goal in enumerate(goals_array):
        if not (hide and goal["done"]):
            print (index+1,goal["name"], (not goal["done"]))

def work_on_goal(array_of_goals):
    clear_screen()
    selected_goal =  get_user_to_select_a_goal(array_of_goals)
    if selected_goal==None: 
        print("not found")
        return 
    clear_screen()
    print("cool lets work on \n", selected_goal["name"])
    
    print("\n\na. add more sub tasks \nb. work on one of the sub goals\nc. hide or unhide a sub-goal\n")
    if len(selected_goal["subgoals"])>0:
        print("we have")
        for index,subgoal in enumerate(selected_goal["subgoals"]):
            print(" -",subgoal["name"])
    choice = input("\nchoose from a,b,c or q: ")
    clear_screen()
    if choice =="b":
         work_on_goal(selected_goal["subgoals"])
    if choice == "c":
        toggle_hide(selected_goal["subgoals"])
    if choice == "a":
        print(f"{selected_goal['name']} \n make a list of everything you can think of, that you can do to achieve: \n {selected_goal['name']}")
        todo = "a"
        while todo !="q":
            todo = input("you can:\n")
            if todo =="q": return
            sub_goal = Goal(todo)
            
            selected_goal["subgoals"].append(sub_goal)
            save_to_database()

        clear_screen()
    if choice == "q":
        return
    else:
        print("please make the correct selection")
        sleep(1)
        return
        
def get_user_to_select_a_goal(array_of_goals,verb="work on"):
    hide = True if verb == "work on" else False
    print(f"please select a goal to {verb} from the following")
    print_all_goals(array_of_goals,hide)
    selection = input()
    if selection == "q": return
    return array_of_goals[int(selection)-1]



def add_new_goal():
    clear_screen()
    goal_title = input("enter title of new goal\n")
    if goal_title == 'q': return main()
    new_goal = Goal(goal_title)
    
    main_goals_array.append(new_goal)
    save_to_database()
    print("added", goal_title)
    sleep(0.3)
    return add_new_goal()

def main():
    selection = "a"
    while selection != 'q':
        if selection == "2":
           add_new_goal()
        # elif selection == "1":
        #     print("here is a list of your goals\nid name")
        #     print_all_goals(main_goals_array)
        elif selection == "3":
            work_on_goal(main_goals_array)
        elif selection == "6":
            toggle_hide(main_goals_array)
        # sleep(1)
        clear_screen()
        selection = input('\nPlease select from the following: \
        \n2. add new goal \
        \n3. work on a goal\
        \n6. hide/archive a goal\
        \nq. quit\n')
main()
