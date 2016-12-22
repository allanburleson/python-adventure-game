"""
This file contains all of the definitions for locations, since there are so
many. Most of these are instances of Location, but some are subclasses since
they need specific functions.
"""

from src.classes import *


def start_location():
    for loc in location_storage:
        if loc.start:
            return loc
    assert False, 'No location is marked as the start location.'


class BlackPit(Location):

    def __init__(self):
        super().__init__(name='A mountain of gold and jewels',
                         items=[],
                         creatures=[],
                         exits={},
                         description='You are in a dank, dirty pit. Yo'
                                     'u don\'t know why you are here i'
                                     'nstead of being on a mountain of'
                                     ' gold and jewels.',
                         show_name_when_exit=True,
                         dark=True)
        self.first_time = True

    def give_info(self, full_info, light):
        if self.first_time:
            print('You run towards the amazing riches...without noticing the giant hole at your feet.')
            print()
            self.name = 'Black Pit'
            self.first_time = False
            super().give_info(True, light)
        else:
            super().give_info(full_info, light)


class DarkTunnel(Location):

    def __init__(self):
        super().__init__(name='Dark Tunnel',
                         items=[],
                         creatures=[Orc(), Orc(), Orc(), Orc()],
                         exits={},
                         description='You are in a featureless dark tunnel.',
                         show_name_when_exit=False,
                         dark=True)


bathroom = Location('Bathroom', [ToiletPaper()], [], show_name_when_exit=True)
bathroom.description = 'There is a toilet and a sink here. They seem'\
                       ' out of place since this is 600 B.C.'
home = Location('Home', [Paper(), Lantern()], [],
                show_name_when_exit=True)
home.items[0].description = '''NOTICE:
These lands have recently become infested with the servants of evil.
Currently, the main problem is the Legendary Dragon of Nogard (the LDN),
a very powerful lizard that threatens to destroy everything we live for.
It would be greatly appreciated if you would help exterminate the
creatures currently endangering the world. There may be some reward to
anyone who defeats the Legendary Dragon of Nogard that has been ravaging
the nation.
We have left a weapon for you in a nearby chest that might be locked in
a chest. You may have to break it open. We really didn't plan this very well.'''
home.description = 'You are in a familiar cabin made out of logs. '\
                   'There is a pleasantly warm fire in the fireplace '\
                   'and a comfortable-looking armchair beside it.'
start = Location('Start', [Mirror()], [], history=False, start=True)
start.description = 'You are in a small room with concrete walls and '\
                    'no windows.'
closet = Location('Closet', [Stick()], [], show_name_when_exit=True)
closet.description = 'You are in a closet that is full of cobwebs.'
attic = Location('Attic', [Bread(), HealthPot()], [GiantSpider()],
                 show_name_when_exit=True, dark=True)
attic.description = 'The attic has been obviously unused for many year'\
                    's. There are large spiderwebs everywhere.'
backyard = Location('Backyard', [], [Snail()])
backyard.description = 'You are in the back yard of your house.'
frontyard = Location('Front Yard', [Chest([Sword()], True)], [])
frontyard.description = 'You are in your front yard.'
homenorth = Location('North of Home', [], [], show_name_when_exit=False)
homenorth.description = 'You are at the side of your house.'
homesouth = Location('South of Home', [], [], show_name_when_exit=False)
homesouth.description = 'You are at a side of your house with a window visible.'
creepyforest = Location('Creepy forest', [], [Ghost()], show_name_when_exit=True)
creepyforest.description = 'You are in a spooky forest.'
forest = Location('Forest', [], [Bear()], show_name_when_exit=True)
forest.description = 'You are in a forest. There is a sign that says '\
                     '"This is not the spooky forest of the East. Stay'\
                     ' away from there!"'
blackpit = BlackPit()
dtn = DarkTunnel()
dts = DarkTunnel()
deadend = Location(
    'Dead End', [], [], show_name_when_exit=True)
deadend.description = 'You are at a dead end.'
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
dts.exits = {'north': blackpit, 'south': deadend}
deadend.exits = {'north': dts}
