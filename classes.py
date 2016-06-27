import sys

creatures = []
items = []
locations = []


class Player(object):
    def __init__(self, location):
        assert isinstance(location, Location)
        self.inventory = []
        self.score = 0
        self.visitedPlaces = {}
        for i in locations:
            self.visitedPlaces[i] = False
        self.move(location)

    def take(self, item):
        assert isinstance(item, Item)
        self.inventory.append(item)
        if item in self.location.items:
            self.location.items.remove(item)
        else:
            print('There is no {0} here.'.format(item.name))
        print('{0} taken.'.format(item.name))

    def sayLocation(self):
        print('You are in {0}.'.format(self.location.name))
        
    def move(self, location):
        assert isinstance(location, Location)
        self.location = location
        if not self.visitedPlaces[self.location]:
            self.location.look()
            self.visitedPlaces[self.location] = True
        else:
            print('You are in {0}.'.format(self.location.name))
        
    def die(self):
        print('GAME OVER.')
        print('Your score was {0}.'.format(self.score))
        sys.exit(0)


class Location(object):
    def __init__(self, name, items, creatures, exits=None, description=''):
        '''exit needs to be a list with [n,s,e,w,u,d]'''
        assert type(items) == list
        assert (type(exits) == list and len(exits) == 6) or exits is None
        if exits is not None:
            for i in exits:
                assert isinstance(i, Location) or i is None
        self.name = name
        self.items = items
        self.creatures = creatures
        self.description = description
        locations.append(self)
        self.exits = exits

    def look(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)
        directions = ['north', 'south', 'east', 'west', 'up', 'down']
        if self.exits is not None:
            for i in self.exits:
                if i is not None:
                    print('There is an exit to the {0}.'.format(directions[self.exits.index(i)]))
        else:
            print('There does not appear to be an exit.')
        print()
        if len(self.creatures) > 0:
            for creature in creatures:
                creature.describe()
            print()
        for item in self.items:
            assert item.locDescription != ''
            print(item.locDescription)


class Creature(object):
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        creatures.append(self)
        
    def describe(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)


class Item(object):
    def __init__(self, name, description='', locDescription=''):
        self.name = name
        self.description = description
        self.locDescription = locDescription
        items.append(self)

    def examine(self):
        assert self.description != '', 'There must be a description.'
        print(self.description)