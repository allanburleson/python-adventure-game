import random
import os
import shelve
import sys

from src import utils

Creatures = []
Items = []
Location_Storage = []


class Screen(object):

    def __init__(self):
        pass

    def clrscn(self):
        print("Entered.")
        os.system("clear")

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
        self.hasLight = False
        self.previousDir = None
        self.location.giveInfo(True, self.hasLight)

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

    def canCarry(self, itemToTake):
        weight = itemToTake.weight
        for item in self.inventory:
            weight += item.weight
        # return True if player can carry item
        return weight <= 100

    # Command functions called in game.py

    def take(self, action, noun):
        def takeItem(i):
            self.location.items.remove(i)
            self.inventory.append(i)
            print('{0} taken.'.format(i.name))
        if noun == '':
            print('What do you want to take?')
        else:
            item = utils.getItemFromName(noun, self.location.items, self)
            if item and not isinstance(item, InteractableItem) and \
                    (not self.location.dark or self.hasLight):
                if self.canCarry(item):
                    takeItem(item)
                else:
                    print('You are carrying too much weight already.')
            elif noun == 'all':
                for i in self.location.items[:]:
                    if not isinstance(i, InteractableItem):
                        if self.canCarry(i):
                            takeItem(i)
                        else:
                            print('You are carrying too much weight already.')
                # if len(self.location.items) > 1:
                 #   takeItem(self.location.items[0])
            elif self.location.dark and not self.hasLight:
                print('There\'s no way to tell if that is here because'
                      ' it is too dark.')
            else:
                print('You can\'t pick up {0} {1}.'.format(
                    utils.getIndefArticle(noun), noun))

    def drop(self, action, noun):
        def dropItem(i):
            self.location.items.append(i)
            self.inventory.remove(i)
            print('{} dropped.'.format(i.name))
        if noun == '':
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

    def look(self, action, noun):
        if self.hasLight and not utils.inInventory(Lantern, self):
            self.hasLight = False
        if noun == '' or noun == 'around':
            self.location.giveInfo(True, self.hasLight)
        else:
            item = utils.getItemFromName(noun, self.inventory, self)
            if item:
                if item.name == 'sword':
                    # Make sword glow if an enemy is in an adjacent room
                    glowing = False
                    for i in self.location.creatures:
                        if isinstance(i, Baddie):
                            item.examine(True)
                            return
                    if not glowing:
                        for exit in self.location.exits:
                            for creature in self.location.exits[exit].creatures:
                                if isinstance(creature, Baddie):
                                    item.examine(True)
                                    return
                    if not glowing:
                        item.examine(False)
                else:
                    item.examine()
            else:
                print('You do not have {0}'.format(noun))

    def go(self, action, noun='', Location=None, previousDir=None):
        def fightCheck():
            if len(self.location.creatures) > 0:
                for i in self.location.creatures[:]:
                    if isinstance(i, Baddie):
                        result = self.fight(i)
                        if result[0] == 'retreat':
                            if len(result) > 1:
                                i.hp = result[1]
                            if self.previousDir == 'north':
                                reverseDir = 'south'
                            elif self.previousDir == 'south':
                                reverseDir = 'north'
                            elif self.previousDir == 'west':
                                reverseDir = 'east'
                            elif self.previousDir == 'east':
                                reverseDir = 'west'
                            elif self.previousDir == 'up':
                                reverseDir = 'down'
                            elif self.previousDir == 'down':
                                reverseDir = 'up'
                            elif self.previousDir == 'northwest':
                                reverseDir = 'southeast'
                            elif self.previousDir == 'northeast':
                                reverseDir = 'southwest'
                            elif self.previousDir == 'southwest':
                                reverseDir = 'northeast'
                            elif self.previousDir == 'southeast':
                                reverseDir = 'northwest'
                            else:
                                assert False, 'Somehow non-direction "{}" got through to here.'.format(
                                    noun)
                            self.go('go', reverseDir)
                        else:
                            self.location.creatures.remove(i)
        if self.hasLight and not utils.inInventory(Lantern, self):
            self.hasLight = False
        if Location is not None:
            locToGoTo = Location
            isLoc = True
        else:
            isDirection = False
            isLoc = False
            locToGoTo = None
            for direction in ['north', 'south', 'east', 'west', 'up',
                              'down', 'northwest', 'northeast',
                              'southwest', 'southeast']:
                if direction == noun:
                    isDirection = True
                    self.previousDir = noun
                    break
                elif direction in self.location.exits:
                    if self.location.exits[direction].name.lower() == noun:
                        locToGoTo = self.location.exits[direction]
                        self.previousDir = direction
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
                loc = None
                # loc = self.locations[self.locations.index(
                # self.location.exits[noun])]
                for i in self.locations:
                    if self.location.exits[noun] == i:
                        loc = i
                if loc:
                    for i in self.locations:
                        if i == loc:
                            locToGoTo = i
                            break
            elif isLoc:
                pass
            else:
                print('There is no exit in that direction.')
                return
        if locToGoTo is not None:
            if not isLoc:
                self.previousDir = noun
            self.location = locToGoTo
            if not self.visitedPlaces[self.location]:
                self.location.giveInfo(True, self.hasLight)
                self.visitedPlaces[self.location] = True
            else:
                self.location.giveInfo(False, self.hasLight)
            if (not self.location.dark) or (self.hasLight):
                fightCheck()
        else:
            print('Something went wrong.')

    def help(self, action, noun):
        print('I can only understand what you say if you first type an'
              ' action and then a noun (if necessary).', end='')
        print(' My vocabulary is limited. If one word doesn\'t work,'
              ' try a synonym. If you get stuck, check the documentati'
              'on.')

    def say(self, action, noun):
        if noun == 'xyzzy':
            if utils.inInventory(Mirror, self):
                if self.location.name == 'Start':
                    self.changeScore(1)
                print('You vanished and reappeared in your house.\n')
                self.go(action, noun)
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

    def quit(self, action, noun):
        resp = input('Are you sure you want to quit? Your progress '
                     'will be saved. [Y/n] ')
        if resp.lower().startswith('y') or resp.strip() == '':
            save = shelve.open('save')
            save['player'] = self
            save['Creatures'] = Creatures
            save['locations'] = self.locations
            save['Items'] = Items
            save.close()
            self.die()
        else:
            print('Cancelled.')

    def restart(self, action, noun):
        resp = input('Are you sure you want to restart the game? [y/N] ')
        if resp.lower().startswith('y'):
            for i in os.listdir():
                if i.startswith('save'):
                    os.remove(i)
            print('Now run play.py again.')
            sys.exit(0)

    def show(self, action, noun):
        if noun == 'inventory':
            if len(self.inventory) > 0:
                print('Inventory:')
                for item in self.inventory:
                    if isinstance(item, Food):
                        print('{0}: Restores {1} health.'.format(
                            item.name, item.health))
                    elif isinstance(item, Weapon):
                        print('{0}: Deals {1} damage.'.format(
                            item.name, item.power))
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

    def use(self, action, noun):
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

    def open(self, action, noun):
        chest = None
        for i in self.location.items:
            if isinstance(i, Chest):
                chest = i
                break
        if chest:
            items = chest.open()
            self.location.items += items

    def hit(self, action, noun):
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

    def eat(self, action, noun):
        item = None
        for i in self.inventory:
            if i.name == noun:
                item = i
        if item:
            if isinstance(item, Food):
                print('You ate the {0} and gained {1} health.'.format(
                    item.name, item.health))
                self.health += item.health
                self.inventory.remove(item)
            else:
                print('Sorry, that isn\'t food.')
        else:
            print('You don\'t have that.')

    def light(self, action, noun):
        if utils.inInventory(Lantern, self) and not self.hasLight:
            print('Your lantern bursts in green flame that illuminates'
                  ' the room.')
            self.hasLight = True
            if self.location.dark:
                self.go('go', Location=self.location)
        elif utils.inInventory(Lantern, self):
            print('Your light is already lit.')
        else:
            print('You need a light source!')


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
                         power=30)


class Item(object):

    def __init__(self, name, description, locDescription, weight):
        self.name = name
        self.description = description
        self.locDescription = locDescription
        self.weight = weight
        Items.append(self)

    def examine(self):
        print(self.description)


class InteractableItem(Item):

    def __init__(self, name, description, locDescription, weight):
        super().__init__(name, description, locDescription, weight)


class Chest(InteractableItem):

    def __init__(self, items, locked):
        super().__init__(name='chest',
                         description='You shouldn\'t see this.',
                         locDescription='A treasure chest is on the ground.',
                         weight=100)
        assert type(items) == list
        self.items = items
        self.locked = locked

    def open(self):
        if self.locked:
            print('The chest cannot be opened because it it locked.')
            return []
        else:
            print('The chest is empty now.')
            for item in self.items:
                print(item.locDescription)
            backupItems = self.items[:]
            self.items = []
            return backupItems


class Weapon(Item):

    def __init__(self, name, description, locDescription, weight, power):
        super().__init__(name, description, locDescription, weight)
        assert type(power) == int
        self.power = power


class Sword(Weapon):

    def __init__(self):
        super().__init__(name='sword',
                         description='The sword is small and has an el'
                         'vish look to it.',
                         locDescription='There is a small sword here.',
                         weight=75,
                         power=random.randint(90, 150))

    def examine(self, glowing):
        print(self.description, end='')
        if glowing:
            print(' It is glowing light blue.')
        else:
            print()


class Fist(Weapon):

    def __init__(self):
        super().__init__(name='fist',
                         description='Your fist looks puny, but it\'s'
                         ' better than no weapon.',
                         locDescription='There is a bug if you are '
                         'reading this.',
                         weight=0,
                         power=10)


class Mirror(Item):

    def __init__(self):
        super().__init__(name='magic mirror',
                         description='The mirror is round and you can '
                         'see your reflection clearly. Under the glass'
                         ' is an inscription that says "XYZZY."',
                         locDescription='There is a small mirror lying'
                         ' on the ground.',
                         weight=2)


class ToiletPaper(Item):

    def __init__(self):
        super().__init__(name='toilet paper',
                         description='The toilet paper is labeled "X-t'
                         'raSoft.',
                         locDescription='A roll of toilet paper is in '
                         'the room.',
                         weight=1)


class Stick(Item):

    def __init__(self):
        super().__init__(name='stick',
                         description='The stick is long and thick. It '
                         'looks like it would be perfect '
                         'for bashing things with.',
                         locDescription='There is a random stick on '
                         'the ground.',
                         weight=3)


class Paper(Item):

    def __init__(self, text=''):
        super().__init__(name='paper',
                         description=text,
                         locDescription='On a table is a paper labeled'
                                        ' NOTICE.',
                         weight=1)


class Coconuts(Item):

    def __init__(self):
        super().__init__(name='coconut halves',
                         description='The coconuts make a noise like '
                                     'horse hooves when banged together.',
                         locDescription='Also on the table are two coc'
                                     'onut halves that look like they '
                                     'probably were carried here by a '
                                     'swallow.',
                         weight=2)


class Lantern(Item):

    def __init__(self):
        super().__init__(name='lantern',
                         description='The lantern is black and is powered'
                         ' by an unknown source.',
                         locDescription='There is a lantern here.',
                         weight=5)


class Food(Item):

    def __init__(self, name, description, locDescription, weight, health):
        super().__init__(name, description, locDescription, weight)
        self.health = health


class HealthPot(Food):

    def __init__(self):
        super().__init__(name='health potion',
                         description='The potion looks disgusting but '
                                     'is probably good for you.',
                         locDescription='There is a health potion here.',
                         weight=2,
                         health=100)


class Bread(Food):

    def __init__(self):
        super().__init__(name='bread',
                         description='The bread is slightly stale but '
                         'looks wholesome.',
                         locDescription='There is a loaf of bread.',
                         weight=1,
                         health=30)
