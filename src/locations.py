from src.classes import *

Location_Storage = []

class Location(object):
    def __init__(self, name, items, creatures, exits={},
            description='', showNameWhenExit=False, dark=False):
        # exit needs to be a dict with keys north, south, east, west,
        # up, down
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
        Location_Storage.append(self)
        self.exits = exits
        self.showNameWhenExit = showNameWhenExit
        self.dark = dark

    def giveInfo(self, fullInfo, light):
        assert self.description != '', 'There must be a description.'
        if self.dark and not light:
            print('It is too dark to see anything. However, you are '\
                  'not likely to be eaten by a grue. What do you think'\
                  ' this is, Zork?')
            return
        elif fullInfo:
            print(self.description)
            print()
            # directions = ['north', 'south', 'east', 'west', 'up', 'down']
            for i in self.exits:
                if self.exits[i].showNameWhenExit:
                    if i == 'up' or i == 'down':
                        print('{} is {}.'.format(self.exits[i].name, i))
                    else:
                        print('{} is to the {}.'.format(self.exits[i].name, i))
                else:
                    print('There is an exit {0}.'.format(i))
            if len(self.exits) == 0:
                print('There does not appear to be an exit.')
        else:
            print('You are in {}.'.format(self.name))
        print()

        for item in self.items:
            if item.locDescription != '':
                print(item.locDescription)
            else:
                print('There is {0} {1}'.format(
                           utils.getIndefArticle(item.name) ,item.name))
        if len(self.items) > 0:
            print()
        if len(self.creatures) > 0:
            for creature in self.creatures:
                print('There is {0} {1} here.'.format(
                       utils.getIndefArticle(creature.name), creature.name))
                       
                       
class BlackPit(Location):
    def __init__(self):
        super().__init__(name='A mountain of gold and jewels',
                         items=[],
                         creatures=[],
                         exits={},
                         description='You are in a dank, dirty pit. Yo'\
                                     'u don\'t know why you are here i'\
                                     'nstead of being on a mountain of'\
                                     ' gold and jewels.\nThere is a si'\
                                     'gn on the wall that says "MORIA '\
                                     '(in the Common Tongue, the \'Bl'\
                                     'ack Pit\')."',
                         showNameWhenExit=True,
                         dark=True)
        self.firstTime = True
    def giveInfo(self, fullInfo, light):
        if self.firstTime:
            print('You run towards the amazing riches...without notici'\
                  'ng the giant hole at your feet.')
            print()
            self.name = 'Black Pit'
            self.firstTime = False
            super().giveInfo(True, light)
        else:
            super().giveInfo(fullInfo, light)
            
            
class DarkTunnel(Location):
    def __init__(self):
        super().__init__(name='Dark Tunnel',
                         items=[],
                         creatures=[Orc(), Orc(), Orc(), Orc()],
                         exits={},
                         description='You are in a featureless dark tunnel.',
                         showNameWhenExit=False,
                         dark=True)
                         
            
bathroom = Location('Bathroom', [ToiletPaper()], [], showNameWhenExit=True)
bathroom.description = 'There is a toilet and a sink here. They seem'\
                       ' out of place since this is 600 B.C.'
home = Location('Home', [Paper(), Lantern(), Coconuts()], [], 
                showNameWhenExit=True)
home.items[0].description = '''NOTICE:
Dear bloody pea--I mean subject,
This area has been troubled with all sorts of monsters lately--orcs,
large spiders, ghosts, and other foul creatures. If you would be so kind
as to assist in their destruction, you could be handsomely rewarded. Of
significant note is the robbery of the beloved and most holy Grail. If
you were to recover it, I, Arthur, King of the Britons, would give you
full command of the land of Camelot and all resources within it,
including all of the ham, jam, and spam that is so dear to the knights
that reside there. I will be excited to be rid of that ridi--I mean,
I hope this incentive will help motivate you peasants to follow my
orders. Oh--yes, did I mention that any person found not hunting these
abominations will be executed? I am your King, you see.
King Arthur of the Britons
PS: I have included with this letter a worthy steed.'''
#'''"NOTICE:
#All able-bodied individuals are asked to assist in capturing or
#destroying the Robots of Unusual Size. More commonly knows as ROUS, they
#have been terrorizing humankind for several weeks and already 3000 lives
#have been lost. Visit our headquarters to register and get free 
#ROUS-fighting supplies.

#Here is what popular media outlets have to say about this menace:
#'Robots of Unusual Size? I don't think they exist.'--DPR Daily

#'Well, since the population of the universe is zero, I'm not sure how
#this issue came about. (See Guide chapter 5) Hopefully this will be 
#resolved.'--Zarniwoop, HG2G

#'We extend condolences to all whose friends and family have been harmed
#in these attacks. Many thanks to the RRO which so dilligently protects
#our loved ones.'--Old York Times

#Please await further letters for updates.

#--RRO (ROUS Resistance Organization)"

#Written under this letter is a handwritten note that says:
#"RRO headquarters: sssessw"'''
home.description = 'You are in a familiar cabin made out of logs. '\
                   'There is a pleasantly warm fire in the fireplace '\
                   'and a comfortable-looking armchair beside it.'
start = Location('Start', [Mirror()], [])
start.description = 'You are in a small room with concrete walls and '\
                    'no windows.'
closet = Location('Closet', [Stick()], [], showNameWhenExit=True)
closet.description = 'You are in a closet that is full of cobwebs.'
attic = Location('Attic', [Bread(), HealthPot()], [GiantSpider()],
                 showNameWhenExit=True, dark=True)
attic.description = 'The attic has been obviously unused for many year'\
                    's. There are large spiderwebs everywhere.'
backyard = Location('Backyard', [], [Snail()])
backyard.description = 'You are in the back yard of your house.'
frontyard = Location('Front Yard', [Chest([Sword()], True)], [])
frontyard.description = 'You are in your front yard.'
homenorth = Location('North of Home', [], [], showNameWhenExit=False)
homenorth.description = 'You are at the side of your house.'
homesouth = Location('South of Home', [], [], showNameWhenExit=False)
homesouth.description = 'You are at a side of your house with a window visible.'
creepyforest = Location('Creepy forest', [], [Ghost()], showNameWhenExit=True)
creepyforest.description = 'You are in a spooky forest.'
forest = Location('Forest', [], [Bear()], showNameWhenExit=True)
forest.description = 'You are in a forest. There is a sign that says '\
                     '"This is not the spooky forest of the East. Stay'\
                     ' away from there!"'
blackpit = BlackPit()
dtn = DarkTunnel()
dts = DarkTunnel()
home.exits = {'north': bathroom, 'south': closet, 'east': backyard,
              'west': frontyard, 'up': attic}
bathroom.exits = {'south': home}
closet.exits = {'north': home}
attic.exits = {'down': home}
backyard.exits = {'west': home, 'east': creepyforest,
                  'northwest': homenorth, 'southwest': homesouth}
creepyforest.exits = {'west': backyard}
frontyard.exits = {'east': home, 'west': forest, 'northeast': homesouth,
                   'southeast': homesouth}
forest.exits = {'east': frontyard}
homenorth.exits = {'southwest': frontyard, 'southeast': backyard}
homesouth.exits = {'northwest': frontyard, 'northeast': backyard,
                   'south': blackpit}
blackpit.exits = {'north': dtn, 'south': dts}
dtn.exits = {'south': blackpit}
dts.exits = {'north': blackpit}
