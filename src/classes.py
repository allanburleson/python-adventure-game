import random
import sys

from src import utils

Creatures = []
Items = []
Location_Storage = []


class Player(object):
    def __init__(self, location, startLoc):
        self.inventory = [Fist()]
        self.score = 0
        self.visitedPlaces = {}
        for i in Location_Storage:
            self.visitedPlaces[i] = False
        self.location = startLoc
        self.location.giveInfo()
        self.health = 100

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
                            print('{0}: {1} power'.format(item.name, item.power))
                            weapons.append(item)
                    choice = input('Weapon: ')
                    for i in weapons:
                        if choice == i.name:
                            weapon = i
                            break
                    if weapon is None:
                        typingError()
                        return 'retreat'
                self.health -= baddie.power
                baddie.hp -= weapon.power
                if self.health > 0 and baddie.hp > 0:
                    print('Your health is {0}.'.format(self.health))
                    print('The {0}\'s health is {1}.'.format(baddie.name, baddie.hp))
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

    # Command functions called in game.py

    def take(self, action, noun, hasNoun):
        if not hasNoun:
            print('What do you want to take?')
        else:
            item = utils.getItemFromName(noun, self.location.items, self)
            if item:
                self.location.items.remove(item)
                self.inventory.append(item)
                print('{0} taken.'.format(item.name))
            else:
                print('There is no {0} here.'.format(noun))

    def drop(self, action, noun, hasNoun):
        if not hasNoun:
            print('Say what you want to drop.')
        else:
            if noun == 'fist':
                print('You can\'t drop your own fist, silly!')
                return
            item = utils.getItemFromName(noun, self.inventory, self)
            if item:
                self.inventory.remove(item)
                self.location.items.append(item)
                print('{} dropped.'.format(item.name))
            else:
                print('You do not have a {} to drop.'.format(noun))

    def look(self, action, noun, hasNoun):
        if not hasNoun or noun == 'around':
            self.location.giveInfo()
        else:
            item = utils.getItemFromName(noun, self.inventory, self)
            if item:
                item.examine()
            else:
                print('You do not have {0}'.format(noun))

    def go(self, action, noun='', hasNoun=None, Location=None):
        if Location is not None:
            self.location = Location
            if not self.visitedPlaces[self.location]:
                self.location.giveInfo()
                self.visitedPlaces[self.location] = True
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
            elif action == 'say':
                # Get right Location from list called locations
                for i in Location_Storage:
                    if i.name == 'Home':
                        locToGoTo = i
                        break
            elif noun in self.location.exits :
                # Get right Location from list called locations
                loc = Location_Storage[Location_Storage.index(
                        self.location.exits[noun])]
                for i in Location_Storage:
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
                    previousDir = noun
                self.location = locToGoTo
                if not self.visitedPlaces[self.location]:
                    self.location.giveInfo()
                    self.visitedPlaces[self.location] = True
                else:
                    print('You are in {0}.'.format(self.location.name))
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
                                    assert False, 'Somehow non-direction "{}" got through to here.'.format(noun)
                                self.go('go', reverseDir, hasNoun = 'True')
                            else:
                                self.location.creatures.remove(i)
            else:
                print('Something went wrong.')


    def help(self, action, noun, hasNoun):
        print('I can only understand what you say if you first type an'\
              ' action and then a noun (if necessary).', end='')
        print(' My vocabulary is limited. If one word doesn\'t work,'\
              ' try a synonym. If you get stuck, check the documentati'\
              'on.')
        
    def say(self, action, noun, hasNoun):
        if noun == 'xyzzy':
            if utils.inInventory(Mirror, self):
                if self.location.name == 'Start':
                    self.changeScore(1)
                print('You vanished and reappeared in your house.\n')
                self.go(action, noun, hasNoun)
                for Location in Location_Storage:
                    if Location.name == 'home':
                        self.go(location=Location)
                        break
            else:
                print('There was a flash of light...and your score was'\
                      ' mysteriously lowered by one.')
                self.score -= 1
        else:
            print('You said "{}" but nothing happened.'.format(noun))

    def quit(self, action, noun, hasNoun):
        resp = input('Are you sure you want to quit? Your progress'\
                     'will be deleted. [Y/n] ')
        if resp.lower.startswith('y'):
            self.die()
        else:
            print('Cancelled.')

    def show(self, action, noun, hasNoun):
        if noun == 'inventory':
            if len(self.inventory) > 0:
                print('Inventory:')
                for item in self.inventory:
                    print(item.name)
            else:
                print('There are no items in your inventory.')
        elif noun == 'location':
            print('You are at ' + self.location.name)
        elif noun == 'score':
            print('Your score is {}.'.format(self.score))
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
                print('The mirror exploded. A large shard of glass hit'\
                      ' you in the face.')
                self.die()


class Location(object):
    def __init__(self, name, items, creatures, exits={},
            description='', showNameWhenExit=False):
        # exit needs to be a dict with keys north, south, east, west,
        # up, down
        assert type(items) == list
        assert (type(exits) == dict or exits is None)
        for i in exits:
            assert isinstance(exits[i], Location)
            assert i in ['north', 'south', 'east', 'west', 'up', 'down']
        self.name = name
        self.items = items
        self.creatures = creatures
        self.description = description
        Location_Storage.append(self)
        self.exits = exits
        self.showNameWhenExit = showNameWhenExit

    def giveInfo(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)
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
                print('There is {0} {1} in the room!'.format(
                       utils.getIndefArticle(creature.name), creature.name))
            print()
        for item in self.items:
            if item.locDescription != '':
                print(item.locDescription)
            else:
                print('There is {0} {1}'.format(
                           utils.getIndefArticle(item.name) ,item.name))


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
        assert type(power) == int
        self.power = power


class Orc(Baddie):
    def __init__(self):
        super().__init__(name='orc',
                         hp=50,
                         description='There is an orc in '\
                                     'the room.',
                         power=random.randint(20, 50))



class Item(object):
    def __init__(self, name, description, locDescription):
        self.name = name
        self.description = description
        self.locDescription = locDescription
        Items.append(self)

    def examine(self):
        print(self.description)
        
        
class Weapon(Item):
    def __init__(self, name, description, locDescription, power):
        super().__init__(name, description, locDescription)
        assert type(power) == int
        self.power = power
        
        
class Sword(Weapon):
    def __init__(self):
        super().__init__(name='sword',
                         description='The sword makes you want to '\
                                     'cleave goblin-necks.',
                         locDescription='There is an unsheathed sword '\
                                        'that looks like it would be '\
                                        'very useful in battle.',
                         power=random.randint(90,150))
                         
                         
class Fist(Weapon):
    def __init__(self):
        super().__init__(name='fist',
                         description='Your fist looks puny, but it\'s'\
                                     ' better than no weapon.',
                         locDescription='There is a bug if you are '\
                                        'reading this.',
                         power=10)

class Mirror(Item):
    def __init__(self):
        super().__init__(name='magic mirror',
                         description='The mirror is round and you can '\
                         'see your reflection clearly. Under the glass'\
                         ' is an inscription that says "XYZZY."',
                         locDescription='There is a small mirror lying'\
                                        ' on the ground.')
                                        

class ToiletPaper(Item):
    def __init__(self):
        super().__init__(name='toilet paper',
                         description='The toilet paper is labeled "X-t'\
                                     'raSoft.',
                         locDescription='A roll of toilet paper is in '\
                                        'the room.')
