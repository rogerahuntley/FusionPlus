# Name: Roger Huntley
# Date: August 13, 2023
# Class: IT-140
# Module 7 Project 2

# Storyboard
# The year is 2047, and you have been paid by the mega corporation Fusion+ to perform a security audit of their Toyota building.
# This means walking into the building and trying to get access to top secret information – a designated button in Mr. Toyota’s office is your target.
# You wander around, collecting items for a janitor costume.
# When you are done, you enter Mr. Toyota’s office and grab the red “flag” button, failing the company on the security audit.
# This button is your villain.

# Rooms: 
# Start
# Entryway. This room has a couch, a fern, a receptionist's desk (with no receptionist) and 3 doors.
# 1
# West Offices. Cubicles. Searching around the desks, you find a still-wrapped janitor outfit lying on a desk for a new hire.
# 2
# East Offices. More cubicles. You find half of a broken keycard lying on someone’s desk with a note. The note reads - “This is yours; you should head to HR and get a new one”.
# 3
# Bathroom. In here, you spot the other half of the keycard sticking out of the garbage bin. 
# 4
# This is the break room. Everyone is at lunch, and they are all in here. You cannot go in here without a janitor’s outfit, or they will notice that they do not recognize you.
# You see a microwave, several tables, some lockers, and a bulletin board. The bulletin board has a clipboard you can grab that has the regular janitor scheduling.
# 5
# This is HR’s office. If you have both halves of the broken keycard, you can go here to get a new one. You also get it upgraded to janitor.
# 6
# This is the janitor’s closet. In here, you find the most important part of your costume – the mop. To get in, you need a working card with proper security clearance.
# V
# This is the final room. You cannot enter if your costume is not complete, so you need all items to get in. Once you enter the room, you can press the button and win the game.

# map looks like this:
# 5   V   3 6
# |   |   | |
# 4-start-1-2

### ROOM CLASS ###

class Room:
  def __init__(self, name, connected_rooms, items=[], required_items=[], uses_items=[],  villian_room=False, description = None, searched=False, cant_enter_text=None, failed_enter_text=None, first_visit_text=None, search_text=None, searched_description=None):
    self.has_visited = False
    self.unlocked = False

    self.name = name
    self.description = description or f"You are in the {name}." # default description
    self.connected_rooms = connected_rooms
    self.items = items
    self.required_items = required_items
    self.uses_items = uses_items
    self.searched = searched
    self.cant_enter_text = cant_enter_text
    self.failed_enter_text = failed_enter_text
    self.first_visit_text = first_visit_text
    self.search_text = search_text
    self.searched_description = searched_description
    self.villian_room = villian_room
  
  def missing_items(self, inventory):
    # get needed items using comprehension
    return [item for item in self.required_items if item not in inventory]
  
  def can_unlock(self, inventory):
    unlockable = self.unlocked or len(self.missing_items(inventory)) == 0
    # auto unlock any unlockable rooms. we dont ever want to lock the player out of a room once they have access to it
    if unlockable:
      self.unlocked = True
      return True
    return unlockable
  
  def can_enter(self, inventory):
    return self.can_unlock(inventory)
  
  # prints from check
  def print_can_enter(self):
    print(f"Target Location: {self.name}\nYou can go that way.\n")

  # prints from check
  def print_cant_enter(self):
    print(f"Target Location: {self.name}\nYou can't go that way!")
    if self.cant_enter_text is not None:
      print(f"\n{self.cant_enter_text}\n")

  # prints on failed move
  def print_failed_enter(self):
    print(f"Target Location: {self.name}\nYou can't go that way!")
    if self.failed_enter_text is not None:
      print(f"\n{self.failed_enter_text}\n")
  
  # prints on first
  def print_first_enter(self):
    if self.first_visit_text is not None:
      print(f"\n{self.first_visit_text}\n")

  # prints on search
  def print_search(self):
    if self.search_text is not None:
      print(f"\n{self.search_text}\n")
  
  # checks / provides an alternate description after searching
  def get_searched_description(self):
    if self.searched_description is not None and self.searched:
      return self.searched_description
    else:
      return self.description

  def __str__(self):
    # return room name and location
    toReturn = f"Current Location: {self.name}"
    toReturn += f"\n{self.get_searched_description()}"
    # optionally add items if there are any and the room has been searched
    if self.searched and len(self.items) > 0:
      toReturn += f"\nItem{'s' if len(self.items) > 1 else ''}: {', '.join(self.items)}"
    return toReturn

### BUILD ROOM MAP ###

rooms = {
  "Entryway": Room(
    "Entryway",
    {
      "east": "West Offices",
      "west": "Break Room",
      "north": "Mr. Toyota\'s Office"
    },
    description="The entryway. Looking around, you see that this room has a couch, a fern, a receptionist\'s desk, and 3 doors.\n"\
    "The door on the left is labeled \"Break Room\", the door on the right is labeled \"West Offices\".\n"\
    "The door straight ahead, behind the receptionist\'s desk, and is labeled \"Mr. Toyota\'s Office\".\n"\
    "The note on the desk reads - \"I\'m at lunch. If you need me, I\'ll be in the break room.\"",
  ),
  "West Offices": Room(
    "West Offices",
    {
      "west": "Entryway",
      "east": "East Offices",
      "north": "Bathroom"
    },
    ["Janitor Outfit"],
    description="Cubicles. Rows and rows of cubicles. On one side of the room, you see a doorway leading to more cubicles.\n"\
    "On the other side of the room, you see a doorway leading to the bathroom.\n"\
    "And of course, the way you came in - the entryway.",
    search_text="You search around the desks, and find a still-wrapped janitor outfit lying on a desk for a new hire.",
  ),
  "East Offices": Room(
    "East Offices",
    {
      "west": "West Offices",
      "north": "Janitor\'s Closet"
    },
    ["Broken Keycard - Top"],
    description="More cubicles. There is clearly an extension of the other offices, it looks newly remodeled.\n"\
    "Perhaps they ran out of space. On the far wall, you spot a small hallway with a door labeled \"Janitor\'s Closet\".\n"\
    "The only other exit is the way you came.",
    search_text="You find half of a broken keycard lying on someone\'s desk with a note.\n"\
    "The note reads - \"This is yours; you should head to HR and get a new one\".",
  ),
  "Bathroom": Room(
    "Bathroom",
    {
      "south": "West Offices"
    },
    ["Broken Keycard - Bottom"],
    description="A bathroom. You see a sink, a toilet, and a garbage bin. The only exit is the way you came.",
    search_text="You spot the other half of the keycard sticking out of the garbage bin.",
  ),
  "Break Room": Room(
    "Break Room",
    {
      "east": "Entryway",
      "north": "HR Office"
    },
    ["Clipboard"],
    ["Janitor Outfit"],
    description="You're standing in the break room. Everyone is at lunch, making jokes and eating sandwiches.\n"
    "You're glad you're wearing a janitor\'s outfit, or they might notice that they don't recognize you.\n"
    "You see a microwave, several tables, some lockers, and a bulletin board.",
    cant_enter_text="You hold your ear up to the door and hear the sounds of people talking and eating.\n"\
    "You think about going in, but you realize that you might look suspicious.\n"\
    "There must be a way to pass through unnoticed.",
    failed_enter_text="You hold your ear up to the door and hear the sounds of people talking and eating.\n"\
    "You think about going in, but you realize that you might look suspicious.\n"\
    "There must be a way to pass through unnoticed.",
    search_text="You look around the break room. You see a microwave, several tables, some lockers, and a bulletin board.\n"\
    "You walk over to the bulletin board and see a clipboard with the regular janitor scheduling.",
  ),
  "HR Office": Room(
    "HR Office",
    # "This is HR\'s office. If you have both halves of the broken keycard, you can go here to get a new one. You also get it upgraded to janitor.",
    {
      "south": "Break Room"
    },
    ["Janitor Keycard"],
    ["Broken Keycard - Top", "Broken Keycard - Bottom"],
    uses_items=["Broken Keycard - Top", "Broken Keycard - Bottom"],
    searched=True, # True because the story text includes the "search" part - they give you the keycard
    description="These appear to be the HR offices. You see people typing on keyboards and looking at charts.\n"\
    "There is a door to the break room to the south.",
    cant_enter_text="You peer into the HR Offices. You see people typing on keyboards and looking at charts.\n"\
    "You don't have anything you need, so you decide not to go in.",
    failed_enter_text="You walk into the HR offices. People are typing on keyboards and looking at charts.\n"\
    "You walk up to the front desk and the gentleman behind the desk look up at you and smiles.\n"\
    "You don't know have anything you need, so you walk back out of the office.",
    first_visit_text="You walk into the HR offices. People are typing on keyboards and looking at charts.\n"\
    "You walk up to the front desk and the gentleman behind the desk look up at you and smiles.\n"\
    "You show him the broken keycard and he says \"Oh, I can fix that for you.\"\n"\
    "He takes the keycard and walks into the back room. A few minutes later, he comes back with a new keycard.\n"\
    "He hands it to you and says \"Here you go. I upgraded you to janitor.\"\n"\
    "You thank him and walk out of the office.",
  ),
  "Janitor\'s Closet": Room(
    "Janitor\'s Closet",
    {
      "south": "East Offices"
    },
    ["Mop"],
    ["Janitor Outfit", "Janitor Keycard"],
    description="This is the janitor\'s closet. There are binders of paperwork strewn about, spilling out of the shelves.\n"\
    "You see cleaning supplies in the corner, and a door to the east offices to the south.",
    cant_enter_text="You look at the door and see a keycard reader.\n"\
    "You'll need a working keycard to get in.",
    failed_enter_text="You walk up to the door and try to open it, but it is locked.\n"\
    "You look around and see a keycard reader.\n"\
    "You'll need a working keycard to get in.",
    search_text="You look around the janitor\'s closet and find a mop.",
    first_visit_text="You walk up to the door and try to open it, but it is locked.\n"\
    "You look around and see a keycard reader.\n"\
    "You have a working keycard, so you swipe it and the door opens."
  ),
  "Mr. Toyota\'s Office": Room(
    "Mr. Toyota\'s Office",
    {
      "south": "Entryway"
    },
    [],
    ["Janitor Outfit", "Mop", "Clipboard"],
    villian_room=True,
    description="This is Mr. Toyota\'s office. You see a desk with a computer and a red button on the left.\n"\
    "There is a stack of papers on the right. There is a door to the entryway to the south.",
    cant_enter_text="You peer through the window and see Mr. Toyota sitting at his desk.\n"\
    "He is looking at a computer screen and typing on a keyboard. You see the red button on his left next to a stack of papers.\n"\
    "He turns to look at the window and you duck down quickly. You can't go in there without a complete costume.",
    first_visit_text="You wait until 3:30, when Mr. Toyota leaves for the day. There is a scheduled cleaning at 3:45.\n"\
    "You ask the receptionist if you can clean Mr. Toyota's office. She says \"Sure, go ahead.\"\n"\
    "She gets up and unlocks the door for you. You walk in and see Mr. Toyota's desk.\n"\
    "You walk over to the desk and see a red button on the left. You press it and the computer screen turns on.\n"\
    "A message on the screen says \"Flag captured.\"\n"
    "You walk out of the office and head home. You have successfully captured the flag!\n"\
    "It seems that Fusion+ will have some work to do to improve their security.\n"\
    "Congratulations! You have won the game!\n\nAbout that job offer...",
    failed_enter_text="You walk into Mr. Toyota's office. He looks up at you and says \"Who are you?\"\n"\
    "You say \"I'm the janitor.\"\n"\
    "He says \"No you're not.\"\n"\
    "You say \"Yes I am.\"\n"\
    "He says \"No you're not.\"\n"\
    "You say \"Yes I am.\"\n"\
    "He says \"No you're not!!!\"\n"\
    "He presses the red button and you hear an alarm go off.\n"\
    "You run out of the office and out of the building.\n"\
    "You have failed to capture the flag. Better luck next time.",
  )
}

game_intro = """
Welcome to the Fusion+ Penetration Test Program
You will be presented with a series of challenges to test your skills.
Your mission: enter the office of Mr. Toyota and press the big red button on his desk.
If you can do this without getting caught, you will be rewarded with a job offer."""

instructions = """Instructions:
help                - display this message
move <direction>    - move to a new room
check               - list available directions
check <direction>   - check the room in a direction
search              - search the current room
pickup <item>       - pickup an item
where               - display your current location
exit                - exit the game

Directions: north, south, east, west
Items: The names of items will be displayed in all caps."""

bad_input = """I don't understand that command.
Type 'help' for a list of commands."""

not_ready = "You can't do that yet..."

last_input = ""
has_won = False
has_lost = False

# inventory will just be an array of strings, no complex logic
inventory = []

# easier to store a reference to the current room than to look it up every time
current_room = rooms['Entryway']

### HELPERS ###

# helper method to keep the console looking nice
def print_with_gap(text):
  print(text, end="\n\n")

# prints the current room info
def print_current_room_info():
  print_with_gap(current_room)

# prints the player's inventory if there is any
def print_current_inventory():
  if(len(inventory) > 0):
    print_with_gap(f"You are carrying: {', '.join(inventory)}")

# sets flag to win the game
def win():
  global has_won
  has_won = True
  input("Press ENTER to continue...")
  print() # make a gap

# sets the flag to lose the game
def lose():
  global has_lost
  has_lost = True
  input("Press ENTER to continue...")
  print() # make a gap

### COMMAND LOGIC ###

def check(args):
  # if no direction passed in, print the connected rooms
  if len(args) == 0:
    print_with_gap(f"Directions with rooms: {', '.join(current_room.connected_rooms.keys())}.")
  else:
    # get the first argument
    direction = args[0]
    # check if the direction is in the connected rooms
    if direction not in current_room.connected_rooms:
      print_with_gap("There is nothing in that direction.")
    # if so, print the connected room
    else:
      target_room = rooms[current_room.connected_rooms[direction]]
      if(target_room.can_enter(inventory)):
        target_room.print_can_enter()
      else:
        target_room.print_cant_enter()

def move(args):
  global current_room
  # if no direction passed in, there's nothing to do
  if len(args) == 0:
    print_with_gap("You need to tell me which direction to move.")
  else:
    # get the first argument
    direction = args[0]
    # check if the direction is in the connected rooms
    if direction not in current_room.connected_rooms:
      print_with_gap("You can't go that way!")
    # if so, move to the connected room
    else:
      target_room = rooms[current_room.connected_rooms[direction]]
      # if you can move print that you did
      if(target_room.can_enter(inventory)):
        print(f"You go {direction}.")
        current_room = rooms[current_room.connected_rooms[direction]]
        # if the user has not visited the room before, display special flavor text
        if not current_room.has_visited:
          current_room.has_visited = True
          current_room.print_first_enter()
          # remove items from your inventory when you first enter a room
          for item in current_room.uses_items:
            if item in inventory:
              inventory.remove(item)
        # see if user has won
        if current_room.villian_room:
          win()
      # if the room is the villian room and you dont have the items, you lose
      elif target_room.villian_room:
        target_room.print_failed_enter()
        lose()
      # otherwise print that you can't
      else:
        target_room.print_failed_enter()
        
  # check win condition
  if not has_lost and not has_won:
    # moving can be disorienting, especially if you dont make it to the room
    # but we dont want to print after the user has lost or won
    print_current_room_info()

def search():
  # if not searched and items exist
  if not current_room.searched and len(current_room.items) > 0:
    # print found items
    current_room.print_search()
    print_with_gap(f"You found: {', '.join(current_room.items)}.")
    current_room.searched = True
  # if not searched or no items
  else:
    # do nothing
    print_with_gap("You didn't find anything.")
  print_current_room_info()

def pickup(args):
  # first lets see if there are any items in the room
  if len(current_room.items) == 0:
    print_with_gap("There are no items in this room.")
    return
  
  # we dont need the args separated, so join them back together
  item = " ".join(args)

  # since we have both "Broken Card - top" and "Broken Card - bottom", i'm not going to expect the user to type the whole thing
  # lets just check the first 5 characters
  search_term = item[:5].lower()
  
  # try to find the first item that starts with the search term
  found_item = None
  for room_item in current_room.items:
    # if we find the item, break out of the loop
    if room_item.lower().startswith(search_term):
      found_item = room_item
      break
  
  # if we didn't find anything, tell the user
  if found_item is None:
    print_with_gap("No item found.")
  else:
    # otherwise, add it to the inventory and remove it from the room
    inventory.append(found_item)
    current_room.items.remove(found_item)
    print_with_gap(f"You picked up {found_item}.")
  
  print_current_inventory()

### MAIN LOOP ###

# processes the user input
def process_input(input):
  # split the input into a command and arguments
  full_command = input.lower().split()

  # if there is no input, just error and return
  if len(full_command) == 0:
    print_with_gap(bad_input)
    return

  # the pop gets first and removes from array
  # then we spread
  # command determines what logic to run
  # args might be empty - but it might hold some data - depends on the command and the input
  command, args = [full_command.pop(0), full_command]

  # "switch" statement - if/elif/else
  # triggers the appropriate logic based on the command
  if command == "help":
    print_with_gap(instructions)
  elif command == "win":
    win()
  elif command == "exit":
    pass
  elif command == "search":
    search()
  elif command == "pickup":
    pickup(args)
  elif command == "check":
    check(args)
  elif command == "move":
    move(args)
  elif command == "where":
    print_current_room_info()
    print_current_inventory()
  else:
    # this means the command was not recognized
    # print text explaining the input was bad
    print_with_gap(bad_input)

### START GAME ###

# print starter info
print_with_gap(game_intro)
print_with_gap(instructions)

# have the user interact to accept instructions
# it's nice to have before we hit them with the room info and other stuff
input("Press ENTER to begin...")
print() # make a gap
print_current_room_info()

# keep running
#  in a loop until an exit condition is met
while(last_input != "exit" and not has_won and not has_lost):
  print("What would you like to do?")
  # get next command
  last_input = input()
  print("\n===========================================\n") # make a gap between responses
  # process the command
  process_input(last_input)

### END GAME ###

print("Goodbye!")