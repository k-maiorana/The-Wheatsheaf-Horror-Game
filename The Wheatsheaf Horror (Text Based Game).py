#Kaitlyn Maiorana
#IT140 Intro to Scripting
#20th February 2022

import random
import time

start_location = 'Gate' #setting starting location
items_to_win = 6 #number of items needed for the good ending

#this header plays before both endings
endgame_header = "You descend the rotting wooden steps..." \
                 "\n...The Wheatsheaf Horror turns to meet you, its amber eyes fixated on yours."

#this ending is played if you do not collect all 6 items
bad_ending_text = endgame_header + \
                  "\nYou approach empty-handed, hoping to talk down your friend..." \
                  "\nBut the man you knew has since been lost." \
                  "\nIn stunned silence, you present little resistance as it lays its teeth upon you." \
                  "\nYou can be friends forever now." \
                  "\nGAME OVER"

#this ending is played if you collect all the items
good_ending_text = endgame_header + \
                   "\nYou approach, blade in hand, knowing what must be done." \
                   "\nAs the creature's eyes dart from the weapon to your once-kind eyes, he--it--seems to understand..." \
                   "\nStill, it hurts to lose a friend." \
                   "\nYOU WIN"

rooms = { #setting the rooms and the directions to get to them
    'Gate': {'east': 'Grand Hall'},
    'Grand Hall': {'north': 'Kitchen', 'south': 'Sports Bar', 'east': 'Office'},
    'Kitchen': {'east': 'Scullery', 'south': 'Grand Hall'},
    'Sports Bar': {'north': 'Grand Hall', 'east': 'Supply Closet'},
    'Supply Closet': {'west': 'Sports Bar'},
    'Scullery': {'west': 'Kitchen'},
    'Office': {'west': 'Grand Hall', 'north': 'Basement'},
    'Basement': {'villain': True, 'south': 'Office'},
}

available_items = { #which items you will need to win the game
    'gear': ["Cleaver", "Jacket", "Flashlight"],
    'gadget': ["Opening Day Photo", "Antidote", "Master Key"] #separated into 2 categories
}

player_inventory = { #listing the player's inventory, divided by category
    'gear': [],
    'gadget': []
}

valid_commands = { #list of usable commands
    'go': ['north', 'south', 'east', 'west'], #directionals to move character
    'exit': ['exit'], #leave the game
    'get': ['gear', 'gadget'] #acquire items
}


def print_slow(text: str, interval: int) -> None: #cinematic esque type scrolling
    for line in text.split('\n'):
        time.sleep(interval)
        print(line)


def print_inventory() -> None: #categorizing inventory gear vs gadgets
    print("Inventory:")
    for k, v in player_inventory.items():
        print(f"\t{k.capitalize()}s:{'' if len(v) > 0 else 'empty'}", end='')
        for i in enumerate(v):
            print(f" {i[1]}{',' if i[0] < len(v) - 1 else ''}", end='')
        print()


def place_items(): #instead of tying each item to a room, this generates them randomly except start/end room
    items_list = available_items['gear'] + available_items['gadget']
    random.shuffle(items_list)

    for room in rooms.items(): #making exception of start and end(villain) rooms
        if room[0] == start_location or room[1].keys().__contains__('villain'):
            continue

        if not room[1].keys().__contains__('item'):
            if items_list.__len__() > 0:
                room[1]['item'] = items_list.pop(0)


def get_item_type(item: str) -> str:
    if item in available_items['gear']:
        return 'gear'
    elif item in available_items['gadget']:
        return 'gadget'
    return 'ERROR: Invalid Item'

def try_add_item(room: str, requested_item_type: str) -> bool: #trying to get an item in start or end room
    if room == start_location or rooms[room].keys().__contains__('villain'):
        print("You can't get items in this room!")
        return False

    if not rooms[room].keys().__contains__('item'): #trying to get an item in an eligible room where there are none
        print("There are no items in this room!")
        return False

    this_item = rooms[room]['item'] #trying to get an item type that isn't in this room
    if get_item_type(this_item) != requested_item_type:
        print(f"There is no {requested_item_type} in this room!")
        return False

    player_inventory[get_item_type(this_item)].append(this_item)
    del rooms[room]['item']
    return True


def show_item_in_room(room: str) -> None:

    if rooms[room].keys().__contains__('villain'):
        return

    if not rooms[room].keys().__contains__('item') or room == start_location:
        print("There are no items in this room.")
        return

    this_item = rooms[room]['item']
    print(f"You see {'your ' if get_item_type(this_item) == 'gear' else 'the '}{this_item}.")


def show_commands() -> None: #prints the command list in the beginning
    print("Move by typing \'go\' (without quotes) and the direction you want to move.")
    print("Collect an item with \'get\' (without quotes) and the item type (gear or gadget).")
    print("You may also exit the game by typing \'exit\' (without quotes).")
    print("Valid commands: ", end='')
    for direction in valid_commands['go']:
        print('go ' + direction, end=', ')
    print('get gear, get gadget, exit.')


def parse_input(raw_command: list) -> (str, str): #using raw input to determine commands
    if raw_command[0] in valid_commands.keys():
        parameter = raw_command[1 if raw_command.__len__() > 1 else 0]
        if parameter in valid_commands[raw_command[0]]:
            return raw_command[0], parameter
        print(F"You cannot use the command \'{raw_command[0]}\' with the parameter \'{parameter}\', please try again!")
        return None, None
    print(F"The command \'{raw_command[0]}\' is not recognized.")
    return None, None


def process_command(cmd: str, param: str, room: str) -> str:
    if cmd is not None and param is not None:
        if cmd == 'exit':
            return 'exit'
        if cmd == 'get':
            try_add_item(room, param)
            return room
        if param in rooms[room]:
            print(F"You go {param}.")
            return rooms[room][param]
        print("You can't go that way!")
        return room
    return room


def check_villain_room(room: str) -> bool: #checking the room for the villain
    if 'villain' in rooms[room]:
        return True
    return False


def play_end_sequence(text: str) -> None: #scrolls through the endgame text
    print_slow(text, 2)

    for i in range(5):
        print('.', end='')
        time.sleep(1)
    print()


def villain_meet(room) -> None: #checking for items
    print(f"You enter the {room}.")
    if not len(player_inventory['gear'] + player_inventory['gadget']) >= items_to_win: #if all 6 items are not present
        play_end_sequence(bad_ending_text) #plays the bad ending/loses
        return
    play_end_sequence(good_ending_text) #if all 6 are, the good ending plays


if __name__ == '__main__':

    place_items() #adding items
    print_slow("\nTHE WHEATSHEAF HORROR\n" #intro text
               f"\nYou are Vince Avery, living on the frisks of the New Jersey town of Dorin.\n"
               "Lately, you've heard more tales of things that go bump in the night than usual.\n"
               "\nAlong the way, you discover a wretched virus in its infancy, threatening to upend any\n"
               "stability you once had.\n"
               "\nAt the center of it all, it seems, is the lonely bartender of Wheatsheaf Hall, known\n"
               "as Gerald Stone. Despite an active scene there and many new hires, it seems like no one\n"
               "is talking about it around town.\n"
               "You must gather three pieces of gear and three gadgets to breach the basement of Wheatsheaf\n"
               "Hall, and confront your longtime friend about the strange occurrences.\n"
               f"\nThere's no time to waste, Vince.\n\n", 1)

    show_commands() #printing the game commands
    current_room = start_location #setting the starting location

    while current_room != 'exit':
        if check_villain_room(current_room):
            villain_meet(current_room)
            break

        print('~'*20)
        print(F"\nYou are currently in the {current_room}.") #printing current location

        print_inventory() #printing player inventory
        show_item_in_room(current_room) #shows the item in the room if any
        print("Enter your move:") #prompts the player to make a move

        parsed_command, parsed_parameter = parse_input(input("> ").lower().split())
        current_room = process_command(parsed_command, parsed_parameter, current_room)

    print("\n\nThanks for playing!") #prints after ending to thank player