import random
import os
import shelve
import sys

from src import utils
from src.modes import Mode

Creatures = []
Items = []
Location_Storage = []


class Splash(Mode):
    """The Splash text that appears"""

    def __init__(self, title):
        self.title = title

    def pStart(self):
        print(self.title)
        print("This is the story of a certain development process\n"
              "It wasn't fun.\n")


class Player(object):

    def __init__(self, locations, startLoc):
        self.inventory = [Fist()]
        self.score = 0
        self.visitedPlaces = {}
        self.location = startLoc
        self.locations = locations
        for i in self.locations:
            self.visitedPlaces[i] = False
        self.health = 100
        self.load()
        self.location.giveInfo(True)

    def die(self):
        print('GAME OVER.')
        print('Your score was {0}.'.format(self.score))
        sys.exit(0)

    def sayLocation(self):
        print('You are in {0}.'.format(self.location.name))

    def changeScore(self, amount):
        self.score += amount
        if amount > 0:
            print('Your score was increased by {0}.'.format(amount))
        elif amount < 0:
            print('Your score was decreased by {0}.'.format(amount * -1))

    def fight(self, baddie):
        def typingError():
            print('Since you can\'t type, you\'re forced to retreat.')
            self.changeScore(-1)
        weapon = None
        while True:
            print('What do you want to do?')
            print('1. Attack')
            print('2. Retreat')
            choice = input('#')
            if choice not in ['1', '2']:
                typingError()
                return 'retreat', baddie.hp
            elif choice.startswith('2'):
                print('You cowardly run away.')
                self.changeScore(-1)
                return 'retreat', baddie.hp
            elif choice.startswith('1'):
                if weapon is None:
                    print('Choose your weapon.')
                    weapons = []
                    for item in self.inventory:
                        if isinstance(item, Weapon):
                            print('{0}: {1} power'.format(
                                item.name, item.power))
                            weapons.append(item)
                    choice = input('Weapon: ')
                    for i in weapons:
                        if choice == i.name:
                            weapon = i
                            break
                    if weapon is None:
                        typingError()
                        return 'retreat', baddie.hp
                self.health -= baddie.power
                baddie.hp -= weapon.power
                if self.health > 0 and baddie.hp > 0:
                    print('Your health is {0}.'.format(self.health))
                    print('The {0}\'s health is {1}.'.format(
                        baddie.name, baddie.hp))
                elif self.health < 1 and baddie.hp > 0:
                    print('You died.')
                    self.die()
                elif baddie.hp < 1 and self.health > 0:
                    print('The {0} has been defeated!'.format(baddie.name))
                    self.changeScore(1)
                    return 'win'
                else:
                    print('Both you and the {0} died!'.format(baddie.name))
                    self.die()

    def load(self):
        # if os.path.isfile('save.db') or os.path.isfile('save.dat'):
            # save = shelve.open('save')
            # self = save['player']
            # Location_Storage = save['Location_Storage']
            # Items = save['Items']
            # Creatures = save['Creatures']
            # save.close()
        return

    # Command functions called in game.py

    def take(self, action, noun, hasNoun):
        def takeItem(i):
            self.location.items.remove(i)
            self.inventory.append(i)
            print('{0} taken.'.format(i.name))
        if not hasNoun:
            print('What do you want to take?')
        else:
            item = utils.getItemFromName(noun, self.location.items, self)
            if item and not isinstance(item, InteractableItem) and not self.location.dark:
                takeItem(item)
            elif noun == 'all':
                for i in self.location.items[:]:
                    if not isinstance(i, InteractableItem):
                        takeItem(i)
                # if len(self.location.items) > 1:
                 #   takeItem(self.location.items[0])
            elif self.location.dark:
                print('There\'s no way to tell if that is here because'
                      ' it is too dark.')
            else:
                print(
                    'There is no {0} here that you can pick up.'.format(noun))

    def drop(self, action, noun, hasNoun):
        def dropItem(i):
            self.location.items.append(i)
            self.inventory.remove(i)
            print('{} dropped.'.format(i.name))
        if not hasNoun:
            print('Say what you want to drop.')
        else:
            if noun == 'fist':
                print('You can\'t drop your own fist, silly!')
                return
            item = utils.getItemFromName(noun, self.inventory, self)
            if item:
                dropItem(item)
            elif noun == 'all':
                for i in self.inventory[:]:
                    if i.name != 'fist':
                        dropItem(i)
            else:
                print('You do not have a {} to drop.'.format(noun))

    def look(self, action, noun, hasNoun):
        if not hasNoun or noun == 'around':
            self.location.giveInfo(True)
        else:
            item = utils.getItemFromName(noun, self.inventory, self)
            if item:
                item.examine()
            else:
                print('You do not have {0}'.format(noun))

    def go(self, action, noun='', hasNoun=None, Location=None, previousDir=None):
        def fightCheck():
            if len(self.location.creatures) > 0:
                for i in self.location.creatures:
                    if isinstance(i, Baddie):
                        result = self.fight(i)
                        if result[0] == 'retreat':
                            if len(result) > 1:
                                i.hp = result[1]
                            if previousDir == 'north':
                                reverseDir = 'south'
                            elif previousDir == 'south':
                                reverseDir = 'north'
                            elif previousDir == 'west':
                                reverseDir = 'east'
                            elif previousDir == 'east':
                                reverseDir = 'west'
                            elif previousDir == 'up':
                                reverseDir = 'down'
                            elif previousDir == 'down':
                                reverseDir = 'up'
                            else:
                                assert False, 'Somehow non-direction "{}" got through to here.'.format(
                                    noun)
                            self.go('go', reverseDir, hasNoun='True')
                        else:
                            self.location.creatures.remove(i)
        if Location is not None:
            locToGoTo = Location
            isLoc = True
        else:
            isDirection = False
            isLoc = False
            locToGoTo = None
            for direction in ['north', 'south', 'east', 'west', 'up',
                              'down']:
                if direction == noun:
                    isDirection = True
                    break
                elif direction in self.location.exits:
                    if self.location.exits[direction].name.lower() == noun:
                        isLoc = True
                        locToGoTo = self.location.exits[direction]
                        previousDir = direction
                        break
            if not isDirection and not isLoc and action != 'say':
                print('You must specify a valid direction.')
                return
            elif action == 'say':
                # Get right Location from list called locations
                for i in self.locations:
                    if i.name == 'Home':
                        locToGoTo = i
                        break
            elif noun in self.location.exits:
                # Get right Location from list called locations
<< << << < HEAD
                loc = Location_Storage[Location_Storage.index(
                    self.location.exits[noun])]
                for i in Location_Storage:
                    if i == loc:
                        locToGoTo = i
                        break
== == == =
                loc = None
                # loc = self.locations[self.locations.index(
                        # self.location.exits[noun])]
                for i in self.locations:
                    if self.location.exits[noun].name == i.name:
                        loc = i
                if loc:
                    for i in self.locations:
                        if i == loc:
                            locToGoTo = i
                            break
>>>>>> > d2ea47d381a595e7fc7cda8bdc9fc07819d2b3fd
            elif isLoc:
                pass
            else:
                print('There is no exit in that direction.')
                return
        if locToGoTo is not None:
            if not isLoc:
                previousDir = noun
            self.location = locToGoTo
            if self.location.dark:
                self.location.giveInfo(False)
            else:
                if not self.visitedPlaces[self.location]:
                    self.location.giveInfo(True)
                    self.visitedPlaces[self.location] = True
                else:
                    self.location.giveInfo(False)
                fightCheck()
        else:
            print('Something went wrong.')

    def help(self, action, noun, hasNoun):
        print('I can only understand what you say if you first type an'
              ' action and then a noun (if necessary).', end='')
        print(' My vocabulary is limited. If one word doesn\'t work,'
              ' try a synonym. If you get stuck, check the documentati'
              'on.')

    def say(self, action, noun, hasNoun):
        if noun == 'xyzzy':
            if utils.inInventory(Mirror, self):
                if self.location.name == 'Start':
                    self.changeScore(1)
                print('You vanished and reappeared in your house.\n')
                self.go(action, noun, hasNoun)
                for Location in self.locations:
                    if Location.name == 'home':
                        self.go(location=Location)
                        break
            else:
                print('There was a flash of light...and your score was'
                      ' mysteriously lowered by one.')
                self.score -= 1
        else:
            print('You said "{}" but nothing happened.'.format(noun))

    def quit(self, action, noun, hasNoun):
<<<<<<< HEAD
        resp = input('Are you sure you want to quit? Your progress'
                     'will be deleted. [Y/n] ')
        if resp.lower.startswith('y'):
=======
        resp = input('Are you sure you want to quit? Your progress '\
                     'will be saved. [Y/n] ')
        if resp.lower().startswith('y'):
            save = shelve.open('save')
            save['player'] = self
            save['Creatures'] = Creatures
            save['locations'] = self.locations
            save['Items'] = Items
            save.close()
>>>>>>> d2ea47d381a595e7fc7cda8bdc9fc07819d2b3fd
            self.die()
        else:
            print('Cancelled.')

    def restart(self, action, noun, hasNoun):
        resp = input('Are you sure you want to restart the game? [Y/n] ')
        if resp.lower().startswith('y'):
            try:
                os.remove('save.db')
            except:
                print('Restart failed.')
            print('Now run play.py again.')
            sys.exit(0)

    def show(self, action, noun, hasNoun):
        if noun == 'inventory':
            if len(self.inventory) > 0:
                print('Inventory:')
                for item in self.inventory:
                    if isinstance(item, Food):
                        print('{0}: Restores {1} health.'.format(item.name, item.health))
                    elif isinstance(item, Weapon):
                        print('{0}: Deals {1} damage.'.format(item.name, item.power))
                    else:
                        print(item.name)
            else:
                print('There are no items in your inventory.')
        elif noun == 'location':
            print('You are at ' + self.location.name)
        elif noun == 'score':
            print('Your score is {}.'.format(self.score))
        elif noun == 'health':
            print('You have {} health.'.format(self.health))
        else:
            print('This isn\'t something I can show you.')

    def use(self, action, noun, hasNoun):
        if noun == 'magic mirror':
            hasMirror = False
            for item in self.inventory:
                if isinstance(item, Mirror):
                    hasMirror = True
                    break
            if hasMirror:
                print('The mirror exploded. A large shard of glass hit'
                      ' you in the face.')
                self.die()

    def open(self, action, noun, hasNoun):
        chest = None
        for i in self.location.items:
            if isinstance(i, Chest):
                chest = i
                break
        if chest:
            items = chest.open()
            self.location.items += items

    def hit(self, action, noun, hasNoun):
        chest = None
        for i in self.location.items:
            if isinstance(i, Chest):
                chest = i
                break
        if chest:
            for i in self.inventory:
                stick = True
                if isinstance(i, Stick):
                    stick = True
                    break
            if stick:
                print('You smashed the lock off the chest.')
                chest.locked = False
            else:
                print('You have nothing to break the chest with.')
        else:
            print('Hitting doesn\'t help.')

    def eat(self, action, noun, hasNoun):
        item = None
        for i in self.inventory:
            if i.name == noun:
                item = i
        if item:
            if isinstance(item, Food):
                print('You ate the {0} and gained {1} health.'.format(item.name, item.health))
                self.health += item.health
                self.inventory.remove(item)
            else:
                print('Sorry, that isn\'t food.')
        else:
            print('You don\'t have that.')


    def light(self, action, noun, hasNoun):
        if utils.inInventory(Lantern, self) and self.location.dark:
            self.location.dark = False
            print('Your lantern bursts in green flame that illuminates'\
                  ' the room.')
            self.go('go', self.location.name, True, self.location, 'up')
        elif utils.inInventory(Lantern, self):
            print('The room is already light enough.')
        else:
            print('You need a light source!')



<<<<<<< HEAD
    def giveInfo(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)
        print()
        # directions = ['north', 'south', 'east', 'west', 'up', 'down']
        for i in self.exits:
            if self.exits[i].showNameWhenExit:
                print('{} is to the {}.'.format(self.exits[i].name, i))
            else:
                print('There is an exit {0}.'.format(i))
        if len(self.exits) == 0:
            print('There does not appear to be an exit.')
        print()
        if len(self.creatures) > 0:
            for creature in self.creatures:
                print('There is {0} {1} here.'.format(
                       utils.getIndefArticle(creature.name), creature.name))
            print()
        for item in self.items:
            if item.locDescription != '':
                print(item.locDescription)
            else:
                print('There is {0} {1}'.format(
                    utils.getIndefArticle(item.name), item.name))
=======
>>>>>>> d2ea47d381a595e7fc7cda8bdc9fc07819d2b3fd


class Creature(object):

    def __init__(self, name, hp, description):
        self.name = name
        self.description = description
        self.hp = hp
        Creatures.append(self)

    def describe(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)


class Snail(Creature):
    def __init__(self):
        super().__init__(name='snail',
                         hp=2,
                         description='There is a snail on the ground.')


class Baddie(Creature):

    def __init__(self, name, hp, description, power):
        super().__init__(name, hp, description)
        assert type(power) == int or type(power) == float
        self.power = power


class Orc(Baddie):

    def __init__(self):
        super().__init__(name='orc',
                         hp=50,
                         description='There is an orc in '
                                     'the room.',
                         power=random.randint(20, 50))


class Ghost(Baddie):
    def __init__(self):
        super().__init__(name='ghost',
                         hp=99999999,
                         description='Wooooo',
                         power=0.01)


class GiantSpider(Baddie):
    def __init__(self):
        super().__init__(name='giant spider',
                         hp=500,
                         description='The spider is large and ugly.',
                         power=15)


class Bear(Baddie):
    def __init__(self):
        super().__init__(name='bear',
                         hp=200,
                         description='The bear growls at you.',
                         power = 30)

class Item(object):

    def __init__(self, name, description, locDescription):
        self.name = name
        self.description = description
        self.locDescription = locDescription
        Items.append(self)

    def examine(self):
        print(self.description)


class InteractableItem(Item):
    def __init__(self, name, description, locDescription):
        super().__init__(name, description, locDescription)


class Chest(InteractableItem):
    def __init__(self, items, locked):
        super().__init__(name='chest',
                         description='You shouldn\'t see this.',
                         locDescription='A treasure chest is on the ground.')
        assert type(items) == list
        self.items = items
        self.locked = locked

    def open(self):
        if self.locked:
            print('The chest cannot be opened because it it locked.')
            return []
        else:
            print('Items in chest:')
            for item in self.items:
                print(item.name)
            backupItems = self.items[:]
            self.items = []
            return backupItems


class Weapon(Item):

    def __init__(self, name, description, locDescription, power):
        super().__init__(name, description, locDescription)
        assert type(power) == int
        self.power = power


class Sword(Weapon):

    def __init__(self):
        super().__init__(name='sword',
                         description='The sword makes you want to '
                                     'cleave goblin-necks.',
                         locDescription='There is an unsheathed sword '
                                        'that looks like it would be '
                                        'very useful in battle.',
                         power=random.randint(90, 150))


class Fist(Weapon):

    def __init__(self):
        super().__init__(name='fist',
                         description='Your fist looks puny, but it\'s'
                                     ' better than no weapon.',
                         locDescription='There is a bug if you are '
                                        'reading this.',
                         power=10)


class Mirror(Item):

    def __init__(self):
        super().__init__(name='magic mirror',
                         description='The mirror is round and you can '
                         'see your reflection clearly. Under the glass'
                         ' is an inscription that says "XYZZY."',
                         locDescription='There is a small mirror lying'
                                        ' on the ground.')


class ToiletPaper(Item):

    def __init__(self):
        super().__init__(name='toilet paper',
                         description='The toilet paper is labeled "X-t'
                                     'raSoft.',
                         locDescription='A roll of toilet paper is in '
                                        'the room.')


class Stick(Item):
    def __init__(self):
        super().__init__(name='stick',
                         description='The stick is long and thick. It '\
                                     'looks like it would be perfect '\
                                     'for bashing things with.',
                         locDescription='There is a random stick on '\
                                        'the ground.')


class Paper(Item):
    def __init__(self, text=''):
        super().__init__(name='paper',
                         description=text,
                         locDescription='On a table is a paper labeled'\
                                        ' NOTICE.')


class Lantern(Item):
    def __init__(self):
        super().__init__(name='lantern',
                         description='The lantern is black and is powered'\
                                     ' by an unknown source.',
                         locDescription='There is a lantern here.')


class Food(Item):
    def __init__(self, name, description, locDescription, health):
        super().__init__(name, description, locDescription)
        self.health = health


class Bread(Food):
    def __init__(self):
        super().__init__(name='bread',
                         description='The bread is slightly stale but '\
                                     'looks wholesome.',
                         locDescription='There is a loaf of bread.',
                         health=30)
