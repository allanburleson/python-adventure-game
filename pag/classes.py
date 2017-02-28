"""
Contains most classes used in the game.
"""

import random
import os
import shelve
import sys

from pag import cwd
from pag import sf_name
from pag import utils

Creatures = []
Items = []

mute = False

class GameObject(object):
    def __init__(self, _mute=False):
        global mute
        if _mute == True:
            mute = _mute
        
    def print(self, *args, end='\n', sep=' ', flush=False, file=None):
        if not mute:
            print(*args, end=end, sep=sep, flush=flush, file=file)

class Player(GameObject):
    """
    The class for everything about the player.

    All public methods either return True or False. This value tells the game
    whether the command should increase the number of moves the player has
    taken.
    """

    def __init__(self, locations, location, mute=False):
        super().__init__(mute)
        self.inventory = [Fist()]
        self.score = 0
        self.visited_places = {}
        self.location_stack = []
        self.location = location
        self.locations = locations
        for i in self.locations:
            self.visited_places[i] = False
        self.health = 100
        self.has_light = False
        self.location.give_info(True, self.has_light)
        self.moves = 0

    def __str__(self):
        inventory = '\n'.join(['\t' + item.name for item in self.inventory])
        return f"You are in {self.location.name}.\n" + \
               f"You have {self.health} health points.\n" + \
               f"You have a score of {self.score} points.\n" + \
               "Inventory:\n" + \
               f"{inventory}"

    def die(self, restart=True):
        self.print('GAME OVER.')
        self.print(f'Your score was {self.score}.')
        self.print(f'You used {self.moves} moves.')
        if restart:
            self.restart('', '', True)
        sys.exit(0)

    # Non-public class methods

    def _change_score(self, amount):
        self.score += amount
        if amount > 0:
            self.print(f'Your score was increased by {amount}.')
        elif amount < 0:
            self.print(f'Your score was decreased by {amount * -1}.')
            
    def _typing_error(self):
        self.print('Since you can\'t type, you\'re forced to retreat.')
        self._change_score(-1)
        
    def _fight(self, baddie):
        weapon = None
        while True:
            self.print('What do you want to do?')
            # Enumerate strings
            utils.number_strings("Attack", "Retreat")
            choice = input('#')
            if choice not in ['1', '2']:
                self._typing_error()
                return 'retreat', baddie.hp
            elif choice.startswith('2'):
                self.print('You cowardly run away.')
                self._change_score(-1)
                return 'retreat', baddie.hp
            elif choice.startswith('1'):
                if weapon is None:
                    self.print('Choose your weapon.')
                    weapons = [
                        i for i in self.inventory if isinstance(i, Weapon)]
                    for i in weapons:
                        self.print(f'{i.name}: {i.power} power')
                    choice = input('Weapon: ')
                    for i in weapons:
                        if choice == i.name:
                            weapon = i
                            break
                    if weapon is None:
                        self._typing_error()
                        return 'retreat', baddie.hp
                self.health -= baddie.power
                baddie.hp -= weapon.power
                if self.health > 0 and baddie.hp > 0:
                    self.print(f'Your health is {self.health}.')
                    self.print(f'The {baddie.name}\'s health is {baddie.hp}.')
                elif self.health < 1 and baddie.hp > 0:
                    self.print('You died.')
                    self.die()
                elif baddie.hp < 1 and self.health > 0:
                    self.print(f'The {baddie.name} has been defeated!')
                    self._change_score(1)
                    self.location.items += baddie.die()
                    return 'win'
                else:
                    self.print(f'Both you and the {baddie.name} died!')
                    self.die()
                    
    def _fight_check(self):
        if len(self.location.creatures) > 0:
            for i in self.location.creatures[:]:
                if isinstance(i, Baddie):
                    result = self._fight(i)
                    if result[0] == 'retreat':
                        if len(result) > 1:
                            i.hp = result[1]
                        self.back('', '')
                    else:
                        self.location.creatures.remove(i)

    def _can_carry(self, item_to_take):
        weight = item_to_take.weight
        for item in self.inventory:
            weight += item.weight
        # return True if player can carry item
        return weight <= 100
        
    def _drop_item(self, i):
        self.location.items.append(i)
        self.inventory.remove(i)
        self.print(f'{i.name} dropped.')

    # Functions callable by the player in-game

    def clrscn(self, action, noun):
        utils.clrscn()
        return False

    def take(self, action, noun):
        def take_item(i):
            self.location.items.remove(i)
            self.inventory.append(i)
            self.print(f'{i.name} taken.')

        weightstring = 'You are carrying too much weight already. Try dropping something.'
        if noun == '':
            self.print('What do you want to take?')
        else:
            item = utils.get_item_from_name(noun, self.location.items)
            if item and not isinstance(item, InteractableItem) and \
                    (not self.location.dark or self.has_light):
                if self._can_carry(item):
                    take_item(item)
                    return True
                else:
                    self.print(weightstring)
            elif noun == 'all':
                for i in self.location.items[:]:
                    if not isinstance(i, InteractableItem):
                        if self._can_carry(i):
                            take_item(i)
                        else:
                            self.print(weightstring)
                return True
                # if len(self.location.items) > 1:
                #   takeItem(self.location.items[0])
            elif self.location.dark and not self.has_light:
                self.print('There\'s no way to tell if that is here because'
                      ' it is too dark.')
            else:
                self.print(
                    f'You can\'t pick up {utils.get_indef_article(noun)} {noun}.')
        return False

    def drop(self, action, noun):
        if noun == '':
            self.print('Say what you want to drop.')
        else:
            if noun == 'fist':
                self.print('You can\'t drop your own fist, silly!')
            item = utils.get_item_from_name(noun, self.inventory)
            if item:
                self._drop_item(item)
                return True
            elif noun == 'all':
                for i in self.inventory[:]:
                    if i.name != 'fist':
                        self._drop_item(i)
                return True
            else:
                self.print(f'You do not have a {noun} to drop.')
        return False

    def look(self, action, noun):
        """Display information about the current location or an item."""
        # Disable light if a lantern is not in the inventory
        if self.has_light and not utils.in_inventory(Lantern, self):
            self.has_light = False
        if noun == '' or noun == 'around':
            self.location.give_info(True, self.has_light)
        else:
            item = utils.get_item_from_name(noun, self.inventory)
            if item:
                if item.name == 'sword':
                    # Make sword glow if an enemy is in an adjacent room
                    glowing = False
                    for i in self.location.creatures:
                        if isinstance(i, Baddie):
                            item.examine(True)
                    if not glowing:
                        for i in self.location.exits:
                            for creature in self.location.exits[exit].creatures:
                                if isinstance(creature, Baddie):
                                    item.examine(True)
                                    return
                    if not glowing:
                        item.examine(False)
                else:
                    item.examine()
            else:
                self.print(f'You do not have {noun}')
                return False
        return True

    def go(self, action, noun='', Location=None, history=True):
        if self.has_light and not utils.in_inventory(Lantern, self):
            self.has_light = False
        if Location is not None:
            destination = Location
            is_loc = True
        else:
            is_direction = False
            is_loc = False
            try:
                destination = self.location.exits[noun]
            except KeyError:
                pass
            for direction in ['north', 'south', 'east', 'west', 'up',
                              'down', 'northwest', 'northeast',
                              'southwest', 'southeast']:
                if direction == noun:
                    is_direction = True
                    break
                elif direction in self.location.exits:
                    if self.location.exits[direction].name.lower() == noun:
                        destination = self.location.exits[direction]
                        break
            if not is_direction and not is_loc and action != 'say':
                self.print('You must specify a valid direction.')
                return
            elif action == 'say':
                # Get right Location from list called locations
                for i in self.locations:
                    if i.name == 'Home':
                        destination = i
                        break
            elif noun in self.location.exits:
                # Get right Location from list called locations
                loc = None
                # loc = self.locations[self.locations.index(
                # self.location.exits[noun])]
                for i in self.locations:
                    if self.location.exits[noun] == i:
                        loc = i
                if loc:
                    for i in self.locations:
                        if i == loc:
                            destination = i
                            break
            elif is_loc:
                pass
            else:
                self.print('There is no exit in that direction.')
                return False
        if destination is not None:
            if self.location.history and history:
                self.location_stack.append(self.location)
            self.location = destination
            if not self.visited_places[self.location]:
                self.location.give_info(True, self.has_light)
                self.visited_places[self.location] = True
            else:
                self.location.give_info(False, self.has_light)
            if not mute and  (not self.location.dark) or self.has_light:
                self._fight_check()
        else:
            self.print('Something went wrong.')
            return False
        return True

    def back(self, action, noun):
        try:
            self.go('', '', Location=self.location_stack[-1])
            self.location_stack.pop()
        except IndexError:
            self.print("There is not a previous location you can go to.")
            return False
        return True

    def help(self, action, noun):
        self.print('I can only understand what you say if you first type an action \
                and then a noun (if necessary). My vocabulary is limited. If \
                one word doesn\'t work, try a synonym. If you get stuck, check\
                 the documentation.')
        return False

    def say(self, action, noun):
        if noun == 'xyzzy':
            if utils.in_inventory(Mirror, self):
                if self.location.name == 'Start':
                    self._change_score(1)
                self.print('You vanished and reappeared in your house.\n')
                self.go(action, noun)
            else:
                self.print('There was a flash of light...and your score was'
                      ' mysteriously lowered by one.')
                self.score -= 1
        else:
            self.print(f'You said "{noun}" but nothing happened.')
            return False
        return True

    def quit(self, action, noun):
        """Save progress and exit the game. Run on KeyboardInterrupt."""
        resp = input('Are you sure you want to quit? Your progress '
                     'will be saved. [Y/n] ')
        if resp.lower().startswith('y') or resp.strip() == '':
            self.save()
            self.die(False)
        else:
            self.print('Cancelled.')
        return False
        
    def save(self, action='', noun=''):
        path = f'{cwd}/{sf_name}'
        sf = shelve.open(path)
        sf['player'] = self
        sf['Creatures'] = Creatures
        sf['locations'] = self.locations
        sf['Items'] = Items
        sf.close()
        self.print(f'Progress saved to {path}.')

    def restart(self, action, noun, force=False):
        """Deletes the save file."""
        def reset():
            for i in os.listdir(cwd):
                if i.startswith(sf_name):
                    os.remove(f'{cwd}/{i}')

        if not force:
            resp = input('Are you sure you want to restart the game? [y/N] ')
            if resp.lower().startswith('y'):
                reset()
                self.print('The save file has been deleted.')
        else:
            reset()
        sys.exit(0)

    def i(self, action, noun):
        """Shortened version of "show inventory"
        """
        self.show('show', 'inventory')

    def show(self, action, noun):
        """Gives information about different things."""
        # TODO: Remove redundant ifs
        if noun == 'inventory':
            if len(self.inventory) > 0:
                self.print('Inventory:')
                for item in self.inventory:
                    self.print('\t', end='')
                    if isinstance(item, Food):
                        self.print(item, end=' ')
                    elif isinstance(item, Weapon):
                        self.print(item, end=' ')
                    else:
                        self.print(item.name, end=': ')
                    self.print(f'weighs {item.weight} pounds.')
            else:
                self.print('There are no items in your inventory.')
        elif noun == 'location':
            self.print('You are at ' + self.location.name)
        elif noun == 'score':
            self.print(f'Your score is {self.score}.')
        elif noun == 'health':
            self.print(f'You have {self.health} health.')
        elif noun == 'exits':
            # TODO: Refactor into function
            self.location.display_exits()
        elif noun == "all":
            self.print(self)
        else:
            self.print('This isn\'t something I can show you.')
        return False

    def use(self, action, noun):
        if noun == 'magic mirror':
            has_mirror = False
            for item in self.inventory:
                if isinstance(item, Mirror):
                    has_mirror = True
                    break
            if has_mirror:
                self.print('The mirror exploded. A large shard of glass hit'
                      ' you in the face.')
                self.die()
        return True

    def open(self, action, noun):
        chest = None
        for i in self.location.items:
            if isinstance(i, Chest):
                chest = i
                break
        if chest:
            items = chest.open()
            self.location.items += items
            return True
        return False

    def hit(self, action, noun):
        chest = None
        for i in self.location.items:
            if isinstance(i, Chest):
                chest = i
                break
        if chest:
            for i in self.inventory:
                stick = True
                if i.name == 'stick':
                    stick = True
                    break
            if stick:
                self.print('You smashed the lock off the chest.')
                chest.locked = False
                return True
            else:
                self.print('You have nothing to break the chest with.')
        else:
            self.print('Hitting doesn\'t help.')
        return False

    def eat(self, action, noun):
        item = None
        for i in self.inventory:
            if i.name == noun:
                item = i
        if item:
            if isinstance(item, Food):
                # Ensure that health can't go above 100
                if item.health + self.health > 100:
                    item.health = 100 - self.health
                self.print(
                    f'You ate the {item.name} and gained {item.health} health.')
                self.health += item.health
                self.inventory.remove(item)
                return True
            else:
                self.print('Sorry, that isn\'t food.')
        else:
            self.print('You don\'t have that.')
        return False

    def light(self, action, noun):
        if utils.in_inventory(Lantern, self) and not self.has_light:
            self.print('Your lantern bursts in green flame that illuminates'
                  ' the room.')
            self.has_light = True
            if self.location.dark:
                # history=False so the same location isn't saved back into
                # self.locationStack
                self.go('go', Location=self.location, history=False)
            return True
        elif utils.in_inventory(Lantern, self):
            self.print('Your light is already lit.')
        else:
            self.print('You need a light source!')
        return False


class Creature(GameObject):
    """
    Supply a name, the creature's health, a description, and
    the items it drops. Set dropItems to a dict with the
    format {item: drop chance percentage}
    """

    def __init__(self, name, hp, description, drop_items={}):
        super().__init__()
        self.name = name
        self.description = description
        self.hp = hp
        self.drop_items = drop_items
        Creatures.append(self)

    def describe(self):
        assert self.description != '', 'There must be a description.'
        self.print(self.description)

    def die(self):
        # Run when creature is killed
        items_to_drop = []
        if len(self.drop_items) > 0:
            for i in self.drop_items:
                random_result = random.randint(0, 100)
                if self.drop_items[i] >= random_result > 0:
                    items_to_drop.append(i)
        if len(items_to_drop) > 0:
            self.print(
                f'The {self.name} dropped {", ".join([i.name for i in items_to_drop])} on its death.')
        return items_to_drop


class Baddie(Creature):

    def __init__(self, name, hp, description, power, drop_items={}):
        super().__init__(name, hp, description, drop_items)
        assert type(power) == int or type(power) == float
        self.power = power


class Item(GameObject):
    """ Class used to instantiate Items
        It is the parent class of:
        - InteractableItem
        - Weapon

        Attributes Include:
        - A name (String)
        - A description (String)
        - A local description (String)
          - Used when 'look'ing
        - And a weight

        Methods Include:
        - player.examine()
          - Prints the description of object
    """

    def __init__(self, name, description, loc_description, weight):
        super().__init__()
        self.name = name
        self.description = description
        self.loc_description = loc_description
        self.weight = weight
        Items.append(self)

    def examine(self):
        self.print(self.description)


class Mirror(Item):

    def __init__(self):
        super().__init__(name='magic mirror',
                         description='The mirror is round and you can '
                         'see your reflection clearly. Under the glass'
                         ' is an inscription that says "XYZZY."',
                         loc_description='There is a small mirror lying'
                         ' on the ground.',
                         weight=2)


class InteractableItem(Item):
    """ Class used to instantiate an Item a player can
        interact with (like kicking)

        Attributes Include:
        - A name (String)
        - A description (String)
        - A local description (String)
          - Used when 'look'ing
        - And a weight
    """

    def __init__(self, name, description, loc_description, weight):
        super().__init__(name, description, loc_description, weight)


class Chest(InteractableItem):

    def __init__(self, items, locked):
        super().__init__(name='chest',
                         description='You shouldn\'t see this.',
                         loc_description='A treasure chest is on the ground.',
                         weight=100)
        assert type(items) == list
        self.items = items
        self.locked = locked

    def open(self):
        if self.locked:
            self.print('The chest cannot be opened because it it locked.')
            return []
        else:
            self.print('The chest is empty now.')
            for item in self.items:
                self.print(item.loc_description)
            backup_items = self.items[:]
            self.items = []
            return backup_items


class Weapon(Item):

    def __init__(self, name, description, loc_description, weight, power):
        super().__init__(name, description, loc_description, weight)
        assert type(power) == int
        self.power = power

    def __str__(self):
        return f'{self.name}: Deals {self.power} damage,'


class Fist(Weapon):

    def __init__(self):
        super().__init__(name='fist',
                         description='Your fist looks puny, but it\'s'
                         ' better than no weapon.',
                         loc_description='There is a bug if you are '
                         'reading this.',
                         weight=0,
                         power=10)


class Lantern(Item):

    def __init__(self):
        super().__init__(name='lantern',
                         description='The lantern is black and is powered'
                         ' by an unknown source.',
                         loc_description='There is a lantern here.',
                         weight=5)


class Food(Item):

    def __init__(self, name, description, loc_description, weight, health):
        super().__init__(name, description, loc_description, weight)
        self.health = health

    def __str__(self):
        return f"{self.name}: Restores {self.health} health,"


location_list = []


class Location(GameObject):
    """
    Class used to instantiate objects

    Attributes Include:
     - A name (String)
     - Any items (List)
     - Any creatures (List)
     - Any exits (Dict)
     - A description (String)
     - If the player can use 'back' to return (Bool)
     - If room name should be shown when exiting (Bool)
     - If it's dark (Bool)
     - Whether it is the starting location (Bool)
    """
    def __init__(self, name, items=[], creatures=[], exits={},
                 description='', history=True, show_name_when_exit=False,
                 dark=False, start=False):
        """
        exits needs to be a dict with keys north, south, east, west,
        up, down
        """
        super().__init__()
        
        global location_list

        assert type(items) == list
        assert (type(exits) == dict or exits is None)
        for i in exits:
            assert isinstance(exits[i], Location)
            assert i in ['north', 'south', 'east', 'west', 'up', 'down',
                         'northwest', 'northeast', 'southwest', 'southeast']
        self.name = name
        self.items = items
        self.creatures = creatures
        self.description = description
        location_list.append(self)
        self.exits = exits
        self.history = history
        self.show_name_when_exit = show_name_when_exit
        self.dark = dark
        self.start = start
        if start:
            for loc in location_list:
                if loc.start and loc.name != self.name:
                    assert False, f'Locations {self.name} and {loc.name} are both marked as being the start location.'

    def give_info(self, full_info, light):
        assert self.description != '', 'There must be a description.'
        if self.dark and not light:
            self.print('It is too dark to see anything. However, you are '
                  'not likely to be eaten by a grue. What do you think'
                  ' this is, Zork?')
            return
        elif full_info:
            self.print(self.description)
            self.print()
            self.display_exits()
        else:
            self.print(f'You are in {self.name}.')
        self.print()

        Entity_Stack = []
        # TODO: Refactor
        for item in self.items:
            Entity_Stack.append(item)
            if item.loc_description != '':
                self.print(item.loc_description)
            else:
                if len(Entity_Stack) > 1:
                    if Entity_Stack[-1].name == item.name:
                        self.print(f'There are {len(Entity_Stack)} {item.name}s')
                else:
                    self.print(f'There is {utils.get_indef_article(item.name)} {item.name}')
        if len(self.items) > 0:
            self.print()
        Entity_Stack = []
        if len(self.creatures) > 0:
            for creature in self.creatures:
                Entity_Stack.append(creature)
            if len(Entity_Stack) > 1:
                if Entity_Stack[-1].name == creature.name:
                    self.print(f'There are {len(Entity_Stack)} {creature.name}s here')
            else:
                self.print(f'There is {utils.get_indef_article(creature.name)} {creature.name} here.')

    def display_exits(self):
        for i in self.exits:
            if self.exits[i].show_name_when_exit:
                if i == 'up' or i == 'down':
                    self.print(f'{self.exits[i].name} is {i}.')
                else:
                    self.print(f'{self.exits[i].name} is to the {i}.')
            else:
                self.print(f'There is an exit {i}.')
        if len(self.exits) == 0:
            self.print('There does not appear to be an exit.')
