import random
import matplotlib.pyplot as plt
import folium
import webbrowser
import os

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.spots = {}

    def set_exits(self, exits):
        self.exits = exits

    def set_spots(self, spots):
        self.spots = spots

    def get_description(self):
        return self.description

    def get_exits(self):
        return self.exits

    def get_spots(self):
        return self.spots

class Character:
    def __init__(self, name, gender, race, char_class, fighting_style, special_stat, allocated_stats):
        self.name = name
        self.gender = gender
        self.race = race
        self.char_class = char_class
        self.fighting_style = fighting_style
        self.special_stat = special_stat
        self.stats = self.initialize_stats(char_class, race, allocated_stats)
        self.inventory = []

    def initialize_stats(self, char_class, race, allocated_stats):
        stats = {'strength': 5, 'agility': 5, 'intelligence': 5, 'charisma': 5, 'constitution': 5, 'wisdom': 5}

        for stat, value in allocated_stats.items():
            stats[stat] += value

        class_bonuses = {
            'Blood Fighter': {'strength': 3, 'agility': 2, 'constitution': 3},
            'Eye User': {'intelligence': 4, 'wisdom': 3, 'charisma': 2},
            'Berserker': {'strength': 4, 'constitution': 3, 'agility': 1},
            'Ice Manipulator': {'intelligence': 4, 'wisdom': 3, 'constitution': 2},
            'Electrokinesis User': {'intelligence': 3, 'agility': 3, 'charisma': 3},
            'Butler': {'strength': 3, 'agility': 2, 'wisdom': 3},
            'Knight': {'strength': 4, 'constitution': 3, 'agility': 1}
        }

        race_bonuses = {
            'Human': {'strength': 1, 'agility': 1, 'intelligence': 1, 'charisma': 1, 'constitution': 1, 'wisdom': 1},
            'Werewolf': {'strength': 2, 'agility': 2, 'constitution': 2},
            'Merfolk': {'strength': 1, 'agility': 2, 'wisdom': 2, 'constitution': 2},
            'Cyborg': {'strength': 3, 'constitution': 3, 'intelligence': 2}
        }

        if char_class in class_bonuses:
            for stat, bonus in class_bonuses[char_class].items():
                stats[stat] += bonus

        if race in race_bonuses:
            for stat, bonus in race_bonuses[race].items():
                stats[stat] += bonus

        return stats

    def get_pronouns(self):
        if self.gender.lower() == 'male':
            return {'subject': 'he', 'object': 'him', 'possessive': 'his'}
        elif self.gender.lower() == 'female':
            return {'subject': 'she', 'object': 'her', 'possessive': 'her'}
        else:
            return {'subject': 'they', 'object': 'them', 'possessive': 'their'}

    def display_stats(self):
        pronouns = self.get_pronouns()
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Race: {self.race}")
        print(f"Class: {self.char_class}")
        print(f"Fighting Style: {self.fighting_style}")
        print(f"Special Stat: {self.special_stat}")
        print("Stats:")
        for key, value in self.stats.items():
            print(f"  {key.capitalize()}: {value}")
        print(f"{pronouns['subject'].capitalize()} is ready for the adventure!")

    def display_inventory(self):
        print(f"{self.name}'s Inventory:")
        if self.inventory:
            for item in self.inventory:
                print(f" - {item}")
        else:
            print("Your inventory is empty.")

class Game:
    def __init__(self):
        self.create_character()
        self.create_locality()
        self.current_room = self.locality['lower_manhattan']
        self.is_playing = True

    def create_character(self):
        print("Create your character:")
        name = input("Enter name: ")
        gender = input("Enter gender (male/female/other): ").lower()

        print("Choose race:")
        races = ['Human', 'Werewolf', 'Merfolk', 'Cyborg']
        for i, race in enumerate(races, start=1):
            print(f"{i}. {race}")
        race_choice = int(input("Enter the number corresponding to your choice: "))
        race = races[race_choice - 1]

        classes = []
        if race == 'Human':
            classes = ['Blood Fighter', 'Eye User']
        elif race == 'Werewolf':
            classes = ['Berserker']
        elif race == 'Merfolk':
            classes = ['Ice Manipulator']
        elif race == 'Cyborg':
            classes = ['Electrokinesis User', 'Butler', 'Knight']

        print("Choose class:")
        for i, char_class in enumerate(classes, start=1):
            print(f"{i}. {char_class}")
        class_choice = int(input("Enter the number corresponding to your choice: "))
        char_class = classes[class_choice - 1]

        print("Choose a special stat to develop:")
        special_stats = {
            'Blood Fighter': 'blood power',
            'Eye User': 'all-seeing eye',
            'Berserker': 'rage',
            'Ice Manipulator': 'ice control',
            'Electrokinesis User': 'electric control',
            'Butler': 'mastery of gadgets',
            'Knight': 'combat mastery'
        }
        special_stat = special_stats[char_class]

        fighting_styles = {
            'Blood Fighter': ['Brain Grid Blood Battle Style', 'Big Dipper Blood-Fighting Style', 'Blood Bullet Arts', 'Esmeralda Blood Freeze'],
            'Eye User': ['Enhanced Perception'],
            'Ice Manipulator': ['Ice Control Techniques'],
            'Butler': ['Mastery of Gadgets'],
            'Knight': ['Swordsmanship', 'Shield Defense']
        }

        if char_class == 'Blood Fighter':
            print("Choose fighting style:")
            for i, style in enumerate(fighting_styles[char_class], start=1):
                print(f"{i}. {style}")
            style_choice = int(input("Enter the number corresponding to your choice: "))
            fighting_style = fighting_styles[char_class][style_choice - 1]
        else:
            fighting_style = fighting_styles[char_class][0]

        allocated_stats = {}
        for stat in ['strength', 'agility', 'intelligence', 'charisma', 'constitution', 'wisdom']:
            allocated_stats[stat] = int(input(f"Allocate points to {stat} (0-10): "))

        self.character = Character(name, gender, race, char_class, fighting_style, special_stat, allocated_stats)
        self.character.display_stats()

    def create_locality(self):
        self.locality = {
            'lower_manhattan': Room("Lower Manhattan", "The bustling financial district of New York City."),
            'chinatown': Room("Chinatown", "A vibrant neighborhood with rich cultural heritage."),
            'little_italy': Room("Little Italy", "A charming neighborhood known for its Italian restaurants."),
            'soho': Room("SoHo", "An artistic neighborhood with trendy shops and galleries."),
            'greenwich_village': Room("Greenwich Village", "A bohemian neighborhood with a lively arts scene."),
            'midtown': Room("Midtown", "The heart of New York City with iconic skyscrapers."),
            'upper_west_side': Room("Upper West Side", "A residential area with cultural landmarks."),
            'harlem': Room("Harlem", "A historic neighborhood known for its African-American culture."),
            'queens': Room("Queens", "A diverse borough with a wide range of attractions."),
            'brooklyn': Room("Brooklyn", "A trendy borough with a strong sense of community."),
            'staten_island': Room("Staten Island", "A suburban borough with scenic parks."),
            'upper_east_side': Room("Upper East Side", "An affluent neighborhood with museums and upscale shops.")
        }

        self.locality['lower_manhattan'].set_exits({
            'n': self.locality['chinatown'],
            'w': self.locality['soho'],
            'u': self.locality['upper_east_side']
        })
        self.locality['lower_manhattan'].set_spots({
            'wall_street': "A busy street with numerous financial institutions.",
            'the_battery': "A waterfront park with views of the Statue of Liberty.",
            'the_statue_of_liberty': "Colossal neoclassical sculpture on Liberty Island, a symbol of freedom and democracy.",
            'ellis_island': "Historic gateway for millions of immigrants to the United States."
        })

        self.locality['chinatown'].set_exits({
            's': self.locality['lower_manhattan'],
            'w': self.locality['little_italy'],
            'n': self.locality['queens']
        })
        self.locality['chinatown'].set_spots({
            'mott_street': "A bustling street with traditional Chinese shops and restaurants.",
            'columbus_park': "A community park where locals practice Tai Chi and play mahjong.",
            'manhattan_bridge': "Iconic suspension bridge connecting Manhattan and Brooklyn.",
            'doyers_street': "A curved street known for its history and hidden gems."
        })

        self.locality['little_italy'].set_exits({
            'e': self.locality['chinatown'],
            'w': self.locality['soho']
        })
        self.locality['little_italy'].set_spots({
            'mulberry_street': "A lively street with Italian restaurants and cafes.",
            'san_gennaro_festival': "An annual feast with food, music, and parades.",
            'italian_american_museum': "A museum showcasing Italian-American heritage.",
            'di_palo_fine_foods': "A family-owned shop selling Italian delicacies."
        })

        self.locality['soho'].set_exits({
            'e': self.locality['lower_manhattan'],
            'w': self.locality['greenwich_village']
        })
        self.locality['soho'].set_spots({
            'art_galleries': "Numerous galleries showcasing contemporary art.",
            'designer_shops': "High-end fashion boutiques.",
            'cast_iron_architecture': "Historic buildings with cast iron facades.",
            'trendy_cafes': "Chic cafes popular with artists and tourists."
        })

        self.locality['greenwich_village'].set_exits({
            'e': self.locality['soho'],
            'n': self.locality['midtown']
        })
        self.locality['greenwich_village'].set_spots({
            'washington_square_park': "A vibrant park with a famous arch.",
            'bleecker_street': "A street known for its music venues and bars.",
            'nyu_campus': "The main campus of New York University.",
            'the_stonewall_inn': "Historic LGBTQ+ bar and site of the Stonewall riots."
        })

        self.locality['midtown'].set_exits({
            's': self.locality['greenwich_village'],
            'n': self.locality['upper_west_side'],
            'e': self.locality['upper_east_side']
        })
        self.locality['midtown'].set_spots({
            'times_square': "A major commercial and entertainment hub.",
            'central_park': "A vast urban park with numerous attractions.",
            'empire_state_building': "An iconic skyscraper with an observation deck.",
            'broadway_theatres': "Numerous theatres hosting world-famous shows."
        })

        self.locality['upper_west_side'].set_exits({
            's': self.locality['midtown'],
            'n': self.locality['harlem']
        })
        self.locality['upper_west_side'].set_spots({
            'lincoln_center': "A complex of buildings for performing arts.",
            'american_museum_of_natural_history': "A renowned museum with extensive exhibits.",
            'riverside_park': "A scenic waterfront park.",
            'columbia_university': "An Ivy League university."
        })

        self.locality['harlem'].set_exits({
            's': self.locality['upper_west_side'],
            'e': self.locality['queens']
        })
        self.locality['harlem'].set_spots({
            'apollo_theater': "A famous venue for African-American performers.",
            'sylvia_s_restaurant': "A landmark soul food restaurant.",
            'harlem_renaissance': "A historic period of African-American cultural revival.",
            'strivers_row': "A historic district with beautiful row houses."
        })

        self.locality['queens'].set_exits({
            'w': self.locality['harlem'],
            'e': self.locality['brooklyn']
        })
        self.locality['queens'].set_spots({
            'flushing_meadows': "A large park with sports facilities and museums.",
            'astoria': "A neighborhood known for its diverse cuisine.",
            'rockaway_beach': "A popular beach destination.",
            'moma_ps1': "A contemporary art museum."
        })

        self.locality['brooklyn'].set_exits({
            'w': self.locality['queens'],
            'e': self.locality['staten_island']
        })
        self.locality['brooklyn'].set_spots({
            'brooklyn_bridge': "An iconic bridge connecting Brooklyn and Manhattan.",
            'prospect_park': "A large park with recreational facilities.",
            'dumbo': "A trendy neighborhood with art galleries and boutiques.",
            'brooklyn_museum': "A major art museum."
        })

        self.locality['staten_island'].set_exits({
            'w': self.locality['brooklyn'],
            'e': self.locality['upper_east_side']
        })
        self.locality['staten_island'].set_spots({
            'staten_island_ferry': "A ferry service with views of the Statue of Liberty.",
            'snug_harbor': "A cultural center with gardens and museums.",
            'richmond_town': "A historic village and museum.",
            'great_kills_park': "A large park with beaches and trails."
        })

        self.locality['upper_east_side'].set_exits({
            'w': self.locality['midtown'],
            's': self.locality['lower_manhattan']
        })
        self.locality['upper_east_side'].set_spots({
            'metropolitan_museum_of_art': "A world-famous art museum.",
            'guggenheim_museum': "A renowned modern art museum.",
            'madison_avenue': "A street known for its luxury boutiques.",
            'central_park_zoo': "A small zoo located within Central Park."
        })

    def start(self):
        print("Welcome to the Text-Based Adventure Game!")
        print("Type 'help' to see the list of commands.")
        while self.is_playing:
            self.show_location()
            command = input("Enter a command: ").lower()
            self.parse_command(command)

    def show_location(self):
        print(f"\nYou are in {self.current_room.name}.")
        print(self.current_room.get_description())
        print("You can see the following spots:")
        for spot in self.current_room.get_spots():
            print(f" - {spot.replace('_', ' ').title()}: {self.current_room.get_spots()[spot]}")
        print("You can go to the following exits:")
        for direction in self.current_room.get_exits():
            print(f" - {direction}: {self.current_room.get_exits()[direction].name}")

    def parse_command(self, command):
        if command == 'help':
            self.show_help()
        elif command == 'inventory':
            self.character.display_inventory()
        elif command == 'stats':
            self.character.display_stats()
        elif command.startswith('go '):
            direction = command.split()[1]
            self.move(direction)
        elif command.startswith('examine '):
            spot = command.split()[1].replace(' ', '_')
            self.examine(spot)
        elif command == 'quit':
            self.is_playing = False
            print("Thank you for playing! Goodbye.")
        else:
            print("Unknown command. Type 'help' to see the list of commands.")

    def show_help(self):
        print("List of commands:")
        print(" - help: Show this help message")
        print(" - inventory: Show your inventory")
        print(" - stats: Show your character's stats")
        print(" - go [direction]: Move to a different location (e.g., 'go n')")
        print(" - examine [spot]: Examine a spot in the current location (e.g., 'examine wall_street')")
        print(" - quit: Quit the game")

    def move(self, direction):
        if direction in self.current_room.get_exits():
            self.current_room = self.current_room.get_exits()[direction]
            self.show_location()
        else:
            print("You can't go that way.")

    def examine(self, spot):
        spots = self.current_room.get_spots()
        if spot in spots:
            print(f"You examine {spot.replace('_', ' ').title()}: {spots[spot]}")
        else:
            print("There is nothing interesting here.")

# Start the game
game = Game()
game.start()

def examine(self, spot):
    spots = self.current_room.get_spots()
    if spot in spots:
        print(f"You examine {spot.replace('_', ' ').title()}:")
        # Check for associated actions
        if spot == 'store':
            print("  - Buy items")
            print("  - Browse items")
            choice = input("What would you like to do? ").lower()
            if choice == 'buy':
                # Implement buying functionality here (e.g., display items and handle purchase)
                pass
            elif choice == 'browse':
                # Show available items in the store
                pass
            else:
                print("Invalid choice.")
        else:
            print(spots[spot])
    else:
        print("There is nothing interesting here.")


def parse_command(self, command):
  # Convert to lowercase for easier comparison
  command = command.lower()

  if command == 'help':
    self.show_help()
  elif command == 'inventory':
    self.character.display_inventory()
  # ... other commands ...
  elif command.startswith('go '):
    direction = command.split()[1]
    self.move(direction)
  # ... other commands ...
  else:
    print("Unknown command. Type 'help' to see the list of commands.")


#add items


def move(self, direction):
  if direction in self.current_room.get_exits():
    self.current_room = self.current_room.get_exits()[direction]
    self.show_location()
  else:
    print("You can't go that way.")


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}

    def set_exits(self, exits):
        self.exits = exits

    def get_exits(self):
        return self.exits

    def get_description(self):
        return self.description

class Game:
    def __init__(self):
        self.create_character()
        self.create_locality()
        self.current_room = self.locality['lower_manhattan']
        self.is_playing = True

    def create_character(self):
        # ... character creation logic ...

    def create_locality(self):
        self.locality = {
            'lower_manhattan': Room("Lower Manhattan", "The bustling financial district of New York City."),
            'chinatown': Room("Chinatown", "A vibrant neighborhood with rich cultural heritage."),
            # ... other rooms ...
        }

        # Define exits for each room
        self.locality['lower_manhattan'].set_exits({
            'n': self.locality['chinatown'],
            'w': self.locality['soho'],
            'u': 'upper_east_side'  # Up to upper east side
        })
        # ... define exits for other rooms ...

    def start(self):
        print("Welcome to the Text-Based Adventure Game!")
        print("Type 'help' to see the list of commands.")
        while self.is_playing:
            self.show_location()
            command = input("Enter a command: ").lower()
            self.parse_command(command)

    def show_location(self):
        print(f"\nYou are in {self.current_room.name}.")
        print(self.current_room.get_description())
        print("You can see the following exits:")
        for direction in self.current_room.get_exits():
            print(f" - {direction}")

    def parse_command(self, command):
        # ... other command handling logic ...
        elif command.startswith('go '):
            direction = command.split()[1]
            self.move(direction)
        # ... other command handling logic ...

    def move(self, direction):
        if direction in self.current_room.get_exits():
            self.current_room = self.locality[self.current_room.get_exits()[direction]]
            self.show_location()
        else:
            print("You can't go that way.")
class Item:
    def __init__(self, name, description, effect=None, pickup_condition=None):
        self.name = name
        self.description = description
        self.effect = effect  # Function that applies the item's effect
        self.pickup_condition = pickup_condition  # Function that checks if conditions are met

    def get_description(self):
        return self.description

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []  # List to store items in the room
        self.exits = {}

    # ... other room methods ...

class Character:
    def __init__(self, name):
        self.name = name
        self.inventory = []  # List to store items in the character's inventory
        self.equipped_item = None  # Slot for an equipped item

    # ... other character methods ...

    def pick_up_item(self, room, item_name):
        items = room.get_items()
        for item in items:
            if item.name.lower() == item_name.lower():
                if not item.pickup_condition or item.pickup_condition(self):
                    self.inventory.append(item)
                    room.items.remove(item)
                    print(f"You pick up the {item.name}.")
                    return
                else:
                    print(f"You can't pick up the {item.name} yet.")
                return
        print(f"You can't find a {item_name} here.")

# Example usage
def create_items():
    batteries = Item("batteries", "A set of AA batteries.")
    flashlight = Item("flashlight", "A flashlight (needs batteries).", effect=lambda: print("You shine the flashlight, illuminating the area."), pickup_condition=lambda character: "batteries" in [item.name.lower() for item in character.inventory])
    keycard = Item("keycard", "A keycard that might unlock something...", effect=lambda: print("You scan the keycard, but nothing happens here."))
    return batteries, flashlight, keycard

def place_items(batteries, flashlight, keycard):
  kitchen = Room("Kitchen", "A small kitchen with a dusty drawer.")
  bedroom = Room("Bedroom", "A bedroom with a dusty desk and a locked cabinet.")
  living_room = Room("Living Room", "A cozy living room.", exits={'n': kitchen})
  kitchen.add_item(batteries)  # Batteries in the kitchen drawer
  bedroom.add_item(flashlight)  # Flashlight on the bedroom desk
  bedroom.add_item(keycard)  # Keycard on the bedroom desk
  return living_room

# Sample usage
batteries, flashlight, keycard = create_items()
living_room = place_items(batteries, flashlight, keycard)

# ... Game loop where the player explores rooms ...

# Player enters the Bedroom
if current_room == bedroom:
  print("You see a dusty desk with a flashlight and a keycard.")
  # Player tries to pick up the flashlight
  character.pick_up_item(current_room, "flashlight")


  def create_locality(self):
      self.locality = {
          'lower_manhattan': Room("Lower Manhattan", "A bustling area with Wall Street and the Financial District."),
          # ... other rooms ...
      }

      self.locality['lower_manhattan'].set_exits({
          'n': self.locality['chinatown'],
          'w': self.locality['soho'],
          'u': self.locality['upper_east_side']
      })
      self.locality['lower_manhattan'].set_spots({
          'subway_station': "A busy subway station with trains going in all directions.",
          'financial_district': "The financial heart of the city, home to the Stock Exchange."
      })
      self.locality['lower_manhattan'].set_subrooms({
          'wall_street': Room('Wall Street', "A busy street with numerous financial institutions."),
          'the_battery': Room('The Battery', "A waterfront park with views of the Statue of Liberty."),
          'the_statue_of_liberty': Room('The Statue of Liberty', "A colossal neoclassical sculpture on Liberty Island.")
      })

      # Add items to rooms
      self.locality['lower_manhattan'].add_item(Item("gold coin", "A shiny gold coin."))
      self.locality['lower_manhattan'].add_item(Item("map", "A map of the city."))

class Game:
    def __init__(self):
        self.character = Character()
        self.is_playing = True
        self.create_locality()
        self.current_room = self.locality['lower_manhattan']

    # ... other methods ...

    def pick_up_item(self, item_name):
        item = self.current_room.remove_item(item_name)
        if item:
            self.character.inventory.append(item)
            print(f"You picked up {item_name}.")
        else:
            print(f"No item named {item_name} here.")

    def look(self):
        print(f"\n{self.current_room.name}")
        print(self.current_room.get_description())
        print("Exits: " + ", ".join(self.current_room.get_exits().keys()))
        print("Spots: " + ", ".join(self.current_room.get_spots().keys()))
        print("Subrooms: " + ", ".join(self.current_room.get_subrooms().keys()))
        print("Items: " + ", ".join([item.name for item in self.current_room.get_items()]))

    # Update the process_command method to handle item interactions
    def process_command(self, command):
        words = command.split()
        if len(words) == 0:
            return

        action = words[0]
        if action in ['go', 'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'u', 'd']:
            self.move(action, words[1:] if action == 'go' else [])
        elif action == 'look':
            self.look()
        elif action == 'explore':
            self.explore(words[1:])
        elif action == 'subroom':
            self.move_to_subroom(words[1])
        elif action == 'back':
            self.move_to_parent_room()
        elif action in ['inventory', 'i']:
            self.character.display_inventory()
        elif action == 'stats':
            self.character.display_stats()
        elif action == 'map':
            self.show_locality_map()
        elif action == 'help':
            self.show_instructions()
        elif action == 'quit':
            self.is_playing = False
            print("Thanks for playing! Goodbye.")
        elif action == 'pick':
            if len(words) > 1:
                self.pick_up_item(" ".join(words[1:]))
            else:
                print("Specify an item to pick up.")
        else:
            print("Unknown command. Type 'help' for a list of commands.")

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.spots = {}
        self.subrooms = {}
        self.items = []

    def set_exits(self, exits):
        self.exits = exits

    def set_spots(self, spots):
        self.spots = spots

    def set_subrooms(self, subrooms):
        self.subrooms = subrooms

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        return None

    def get_description(self):
        return self.description

    def get_exits(self):
        return self.exits

    def get_spots(self):
        return self.spots

    def get_subrooms(self):
        return self.subrooms

    def get_items(self):
        return self.items

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_description(self):
        return self.description

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.spots = {}
        self.subrooms = {}
        self.items = []
        self.sublocations = {}

    def set_exits(self, exits):
        self.exits = exits

    def set_spots(self, spots):
        self.spots = spots

    def set_subrooms(self, subrooms):
        self.subrooms = subrooms

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        return None

    def add_sublocation(self, name, sublocation):
        self.sublocations[name] = sublocation

    def get_description(self):
        return self.description

    def get_exits(self):
        return self.exits

    def get_spots(self):
        return self.spots

    def get_subrooms(self):
        return self.subrooms

    def get_items(self):
        return self.items

    def get_sublocations(self):
        return self.sublocations

class Sublocation:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        return None

    def get_description(self):
        return self.description

    def get_items(self):
        return self.items

class Game:
    def __init__(self):
        self.character = Character()
        self.is_playing = True
        self.create_locality()
        self.current_room = self.locality['lower_manhattan']
        self.current_subroom = None
        self.current_sublocation = None

    # ... other methods ...

    def move_to_sublocation(self, sublocation_name):
        if self.current_subroom and sublocation_name in self.current_subroom.get_sublocations():
            self.current_sublocation = self.current_subroom.get_sublocations()[sublocation_name]
            print(f"\nYou move to {sublocation_name}.")
            self.look()
        else:
            print(f"No sublocation named {sublocation_name} here.")

    def move_to_parent_subroom(self):
        if self.current_sublocation:
            self.current_sublocation = None
            print("\nYou move back to the subroom.")
            self.look()
        else:
            print("You are not in a sublocation.")

    def pick_up_item(self, item_name):
        if self.current_sublocation:
            item = self.current_sublocation.remove_item(item_name)
        elif self.current_subroom:
            item = self.current_subroom.remove_item(item_name)
        else:
            item = self.current_room.remove_item(item_name)

        if item:
            self.character.inventory.append(item)
            print(f"You picked up {item_name}.")
        else:
            print(f"No item named {item_name} here.")

    def look(self):
        if self.current_sublocation:
            print(f"\n{self.current_sublocation.name}")
            print(self.current_sublocation.get_description())
            print("Items: " + ", ".join([item.name for item in self.current_sublocation.get_items()]))
        elif self.current_subroom:
            print(f"\n{self.current_subroom.name}")
            print(self.current_subroom.get_description())
            print("Sublocations: " + ", ".join(self.current_subroom.get_sublocations().keys()))
            print("Items: " + ", ".join([item.name for item in self.current_subroom.get_items()]))
        else:
            print(f"\n{self.current_room.name}")
            print(self.current_room.get_description())
            print("Exits: " + ", ".join(self.current_room.get_exits().keys()))
            print("Spots: " + ", ".join(self.current_room.get_spots().keys()))
            print("Subrooms: " + ", ".join(self.current_room.get_subrooms().keys()))
            print("Items: " + ", ".join([item.name for item in self.current_room.get_items()]))

    def process_command(self, command):
        words = command.split()
        if len(words) == 0:
            return

        action = words[0]
        if action in ['go', 'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'u', 'd']:
            self.move(action, words[1:] if action == 'go' else [])
        elif action == 'look':
            self.look()
        elif action == 'explore':
            self.explore(words[1:])
        elif action == 'subroom':
            self.move_to_subroom(words[1])
        elif action == 'sublocation':
            self.move_to_sublocation(words[1])
        elif action == 'back':
            if self.current_sublocation:
                self.move_to_parent_subroom()
            else:
                self.move_to_parent_room()
        elif action in ['inventory', 'i']:
            self.character.display_inventory()
        elif action == 'stats':
            self.character.display_stats()
        elif action == 'map':
            self.show_locality_map()
        elif action == 'help':
            self.show_instructions()
        elif action == 'quit':
            self.is_playing = False
            print("Thanks for playing! Goodbye.")
        elif action == 'pick':
            if len(words) > 1:
                self.pick_up_item(" ".join(words[1:]))
            else:
                print("Specify an item to pick up.")
        else:
            print("Unknown command. Type 'help' for a list of commands.")

def create_locality(self):
    self.locality = {
        'lower_manhattan': Room("Lower Manhattan", "A bustling area with Wall Street and the Financial District."),
        'central_park': Room("Central Park", "A large public park in New York City.")
        # ... other rooms ...
    }

    self.locality['lower_manhattan'].set_exits({
        'n': self.locality['chinatown'],
        'w': self.locality['soho'],
        'u': self.locality['upper_east_side']
    })
    self.locality['lower_manhattan'].set_spots({
        'subway_station': "A busy subway station with trains going in all directions.",
        'financial_district': "The financial heart of the city, home to the Stock Exchange."
    })
    self.locality['lower_manhattan'].set_subrooms({
        'wall_street': Room('Wall Street', "A busy street with numerous financial institutions."),
        'the_battery': Room('The Battery', "A waterfront park with views of the Statue of Liberty."),
        'the_statue_of_liberty': Room('The Statue of Liberty', "A colossal neoclassical sculpture on Liberty Island.")
    })

    self.locality['central_park'].set_exits({
        's': self.locality['lower_manhattan'],
        'w': self.locality['upper_west_side'],
        'e': self.locality['upper_east_side']
    })
    self.locality['central_park'].set_subrooms({
        'lake': Room('The Lake', "A large lake in Central Park, popular for boating."),
        'pond': Room('The Pond', "A tranquil pond surrounded by trees and wildlife."),
        'information_center': Room('Information Center', "A center with maps and information about the park.")
    })

    lake_sublocations = {
        'boathouse': Sublocation('Boathouse', "A place where you can rent boats and take a ride on the lake."),
        'picnic_area': Sublocation('Picnic Area', "A nice spot to have a picnic by the lake.")
    }
    for name, sublocation in lake_sublocations.items():
        self.locality['central_park'].get_subrooms()['lake'].add_sublocation(name, sublocation)

    self.locality['central_park'].get_subrooms()['lake'].add_item(Item("boat", "A small rowboat for exploring the lake."))
    self.locality['central_park'].get_subrooms()['pond'].add_item(Item("duck_feed", "A bag of feed for feeding the ducks."))
    self.local

def create_locality(self):
    self.locality = {
        'lower_manhattan': Room("Lower Manhattan", "A bustling area with Wall Street and the Financial District."),
        'central_park': Room("Central Park", "A large public park in New York City.")
        # ... other rooms ...
    }

    self.locality['lower_manhattan'].set_exits({
        'n': self.locality['chinatown'],
        'w': self.locality['soho'],
        'u': self.locality['upper_east_side']
    })
    self.locality['lower_manhattan'].set_spots({
        'subway_station': "A busy subway station with trains going in all directions.",
        'financial_district': "The financial heart of the city, home to the Stock Exchange."
    })
    self.locality['lower_manhattan'].set_subrooms({
        'wall_street': Room('Wall Street', "A busy street with numerous financial institutions."),
        'the_battery': Room('The Battery', "A waterfront park with views of the Statue of Liberty."),
        'the_statue_of_liberty': Room('The Statue of Liberty', "A colossal neoclassical sculpture on Liberty Island.")
    })

    self.locality['central_park'].set_exits({
        's': self.locality['lower_manhattan'],
        'w': self.locality['upper_west_side'],
        'e': self.locality['upper_east_side']
    })
    self.locality['central_park'].set_subrooms({
        'lake': Room('The Lake', "A large lake in Central Park, popular for boating."),
        'pond': Room('The Pond', "A tranquil pond surrounded by trees and wildlife."),
        'information_center': Room('Information Center', "A center with maps and information about the park.")
    })

    lake_sublocations = {
        'boathouse': Sublocation('Boathouse', "A place where you can rent boats and take a ride on the lake."),
        'picnic_area': Sublocation('Picnic Area', "A nice spot to have a picnic by the lake.")
    }
    for name, sublocation in lake_sublocations.items():
        self.locality['central_park'].get_subrooms()['lake'].add_sublocation(name, sublocation)

    self.locality['central_park'].get_subrooms()['lake'].add_item(Item("boat", "A small rowboat for exploring the lake."))
    self.locality['central_park'].get_subrooms()['pond'].add_item(Item("duck_feed", "A bag of feed for feeding the ducks."))
    self.locality['central_park'].get_subrooms()['information_center'].add_item(Item("map", "A detailed map of Central Park."))

    self.locality['lower_manhattan'].add_item(Item("gold coin", "A shiny gold coin."))
    self.locality['lower_manhattan'].add_item(Item("map", "A map of the city."))

class Brownstone1_AffluentFamilyHome:
    def __init__(self):
        self.description = "This grand brownstone boasts several floors and high-tech features, catering to a family of four and their canine companion."
        self.ground_floor = {
            "Entrance Foyer": "High-tech security system with retinal scanner and holographic welcome message.",
            "Smart Mudroom": "Boot dryers for wet weather, automated dog washing station with grooming options, ample storage for sports equipment and outdoor gear.",
            "Two-Car Garage": "Charging stations for electric vehicles, built-in workshop area for tinkering with personal vehicles."
        }
        self.first_floor = {
            "Open-Plan Living Area": "Expansive living room with retractable walls opening onto a balcony overlooking a landscaped rooftop garden.",
            "Gourmet Kitchen": "Voice-activated appliances, customizable countertops that adjust for food prep (chopping block, pizza oven), hidden pet feeding station.",
            "Dog Run Room": "Indoor play area with climate control and waste disposal system."
        }
        self.second_floor = {
            "Master Suite": "Luxurious bedroom with a spa-like bathroom featuring a chromatherapy shower and a rejuvenating soaking tub. Walk-in closet with automated clothing organization and climate control.",
            "Children's Bedrooms": "Themed rooms with interactive features (holographic jungle gym, virtual reality gaming area), connected by a Jack-and-Jill bathroom with double showers."
        }
        self.third_floor = {
            "Family Room": "Large entertainment space with a home theater system, comfortable seating that folds out into guest beds.",
            "Study/Office": "Soundproofed room with ergonomic furniture and multiple workstations for remote work or hobbies.",
            "Rooftop Garden": "Urban oasis with a hydroponic vegetable garden, solar panels for generating clean energy, and a designated space for the family dog to safely enjoy the outdoors."
        }

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_picked_up = False

    def pick_up(self):
        self.is_picked_up = True
        return f"You have picked up {self.name}."

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.connected_rooms = {}

    def add_item(self, item):
        self.items.append(item)

    def connect_room(self, direction, room):
        self.connected_rooms[direction] = room

class Game:
    def __init__(self):
        self.brownstone1 = Brownstone1_AffluentFamilyHome()
        self.current_room = None

    def start(self):
        self.current_room = Room("Entrance Foyer", self.brownstone1.ground_floor["Entrance Foyer"])

    def move(self, direction):
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            return f"You moved to {self.current_room.name}."
        else:
            return "You can't move in that direction."

    def look_around(self):
        return self.current_room.description

    def pick_up_item(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                return item.pick_up()
        return "Item not found."

# Example usage
game = Game()
game.start()
print(game.look_around())  # "High-tech security system with retinal scanner and holographic welcome message."


class Brownstone2_ConvertedDuplexPenthouse:
    def __init__(self):
        self.description = "This brownstone showcases the flexibility of brownstone conversions."
        self.ground_floor = {
            "Shared Entrance": "Secure entryway with video intercom system."
        }
        self.duplex_lower_level = {
            "Dr. Anya Kapoor's Apartment": {
                "Medical Suite": "Compact but well-equipped medical suite for consultations and check-ups.",
                "Workshop": "Hidden workshop area stocked with high-end cybernetic implants and customization tools.",
                "Living Quarters": "Private living quarters with a minimalist design and a small balcony overlooking the street."
            }
        }
        self.duplex_upper_level = {
            "Kai Singh's Apartment": {
                "Living Area": "Open-plan living area with a VR workstation dedicated to brain dance customization.",
                "Biohacking Lab": "Biohacking lab for tinkering with neural interfaces and other tech.",
                "Relaxation Room": "Relaxation room with mood lighting and a sensory deprivation pod."
            }
        }
        self.penthouse = {
            "Living Area": "Breathtaking city views, wraparound balcony with access from multiple rooms.",
            "Smart Kitchen": "High-end appliances with personalized settings for each resident.",
            "Dual Master Suites": "Each with luxurious amenities and en-suite bathrooms.",
            "Rooftop Terrace": "Private outdoor space with a jacuzzi, solar panels, and a small greenhouse."
        }

class Brownstone3_ConvertedMultiUnit:
    def __init__(self):
        self.description = "This converted brownstone exemplifies the diverse living situations found in NYC."
        self.basement = {
            "Ripperdoc's Den": "Dr. 'Chop' Choi's illegal clinic offering black market cyberware installations and body modifications. Hidden entrance accessible through a secret door in an alleyway."
        }
        self.ground_floor = {
            "Paramedic Mom and Son": {
                "Apartment": "Compact but functional apartment with durable furniture and easy-to-clean surfaces.",
                "Workspace": "Dedicated workspace for the paramedic mom and a gaming area for her teenage son."
            }
        }
        self.first_floor = {
            "Grieving Widower": "Cozy apartment with warm lighting and sentimental decorations reminding him of his late wife. Quiet reading nook and a small balcony overlooking a community garden."
        }
        self.second_floor = {
            "Young Couple": "Open-plan apartment with mismatched furniture reflecting their different styles. One room is still mostly unpacked, showing they're adjusting to living together."
        }
        self.third_floor = {
            "Weed Enthusiast's Paradise": "Sun-drenched apartment overflowing with plant life. Vertical gardens lining the walls, automated watering systems, and a rooftop greenhouse accessible through a skylight."
        }
class MuseumOfNaturalHistory:
    def __init__(self):
        self.floors = {
            "Floor 1": {
                "Theodore Roosevelt Memorial Hall": "The heart of the museum with grand displays and historical exhibits.",
                "Ocean Life": "Exhibits on marine biology and ecosystems.",
                "North American Mammals": "Displays of mammal species from North America.",
                # Add more rooms as needed
            },
            "Floor 2": {
                "African Mammals": "Exhibits on mammals native to Africa.",
                "Asian Mammals": "Displays of mammal species from Asia.",
                "Birds of the World": "A comprehensive collection of bird species from around the globe.",
                # Add more rooms as needed
            },
            "Floor 3": {
                "African Mammals": "Exhibits on mammals native to Africa.",
                "North American Birds": "Displays of bird species from North America.",
                "Reptiles and Amphibians": "Exhibits on various reptiles and amphibians.",
                # Add more rooms as needed
            },
            "Floor 4": {
                "Saurischian Dinosaurs": "Displays of Saurischian dinosaur fossils.",
                "Ornithischian Dinosaurs": "Exhibits on Ornithischian dinosaur species.",
                "Advanced Mammals": "Displays of advanced mammal species.",
                # Add more rooms as needed
            },
            "Lower Level": {
                "Rose Center for Earth and Space": "Exhibits on space exploration and astronomy.",
                "Gilder Center": "Exhibits on science, education, and innovation.",
                # Add more rooms as needed
            }
        }
        self.current_floor = "Floor 1"
        self.current_room = "Theodore Roosevelt Memorial Hall"

    def move(self, floor, room):
        if floor in self.floors and room in self.floors[floor]:
            self.current_floor = floor
            self.current_room = room
            return f"You moved to {room} on {floor}."
        else:
            return "You can't move to that location."

    def look_around(self):
        return self.floors[self.current_floor][self.current_room]

# Example usage
museum = MuseumOfNaturalHistory()
print(museum.look_around())  # "The heart of the museum with grand displays and historical exhibits."
