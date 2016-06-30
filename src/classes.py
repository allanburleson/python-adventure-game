import sys

from src import utils

Creatures = []
Items = []
Location_Storage = []


class Player(object):
    def __init__(self, location, startLoc):
        self.inventory = []
        self.score = 0
        self.visitedPlaces = {}
        for i in Location_Storage:
            self.visitedPlaces[i] = False
        self.location = startLoc
        self.location.giveInfo()

    def die(self):
        print('GAME OVER.')
        print('Your score was {0}.'.format(self.score))
        sys.exit(0)

    def sayLocation(self):
        print('You are in {0}.'.format(self.location.name))

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
            for direction in ['north', 'south', 'east', 'west', 'up', 
                              'down']:
                if direction == noun:
                    isDirection = True
                    break
            locToGoTo = None
            if not isDirection and action != 'say':
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
            else:
                print('There is no exit in that direction.')
                return
            if locToGoTo is not None:
                self.location = locToGoTo
                if not self.visitedPlaces[self.location]:
                    self.location.giveInfo()
                    self.visitedPlaces[self.location] = True
                else:
                    print('You are in {0}.'.format(self.location.name))
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
                if self.location.name == 'start':
                    self.score += 1
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
            if self.showNameWhenExit:
                print('{} is to the {}.'.format(self.exits[i].name, i))
            else:
                print('There is an exit {0}.'.format(i))
        if len(self.exits) == 0:
            print('There does not appear to be an exit.')
        print()
        if len(self.creatures) > 0:
            for creature in Creatures:
                creature.describe()
            print()
        for item in self.items:
            if item.locDescription != '':
                print(item.locDescription)
            else:
                print('There is a(n) {}'.format(item.name))


class Creature(object):
    def __init__(self, name, hp, description):
        self.name = name
        self.description = description
        self.hp = hp
        Creatures.append(self)

    def describe(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)


class Baddie(Creature):
    def __init__(self, name, hp, description, power):
        super().__init__(name, hp, description)
        self.power = power


class Orc(Baddie):
    def __init__(self):
        super().__init__(name='orc',
                         hp=100,
                         description='There is a nasty-looking orc in '\
                                     'the room.',
                         power=100)



class Item(object):
    def __init__(self, name, description='', locDescription=''):
        self.name = name
        self.description = description
        self.locDescription = locDescription
        Items.append(self)

    def examine(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)


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
