from src.classes import *

bathroom = Location('Bathroom', [ToiletPaper()], [], showNameWhenExit=True)
bathroom.description = 'There is a toilet and a sink here. They seem'\
                       ' out of place since this is 600 B.C.'
home = Location('Home', [], [], showNameWhenExit=True)
home.description = 'You are in a familiar cabin made out of logs. '\
                   'There is a pleasantly warm fire in the fireplace '\
                   'and a comfortable-looking armchair beside it.'
start = Location('Start', [Mirror()], [])
start.description = 'You are in a small room with concrete walls and '\
                    'no windows.'
closet = Location('Closet', [Stick()], [], showNameWhenExit=True)
closet.description = 'You are in a closet that is full of cobwebs.'
attic = Location('Attic', [Bread()], [GiantSpider()], showNameWhenExit=True)
attic.description = 'The attic has been obviously unused for many year'\
                    's. There are large spiderwebs everywhere.'
backyard = Location('Backyard', [], [Snail()])
backyard.description = 'You are in the backyard of your house.'
frontyard = Location('Front Yard', [Chest([Sword()], True)], [])
frontyard.description = 'You are in your front yard.'
creepyforest = Location('Creepy forest', [], [Ghost()], showNameWhenExit=True)
creepyforest.description = 'You are in a spooky forest.'
forest = Location('Forest', [], [Bear()], showNameWhenExit = True)
forest.description = 'You are in a forest. There is a sign that says '\
                     '"This is not the spooky forest of the East. Stay'\
                     ' away from there!"'
home.exits = {'north': bathroom, 'south': closet, 'east': backyard,
              'west': frontyard, 'up': attic}
bathroom.exits = {'south': home}
closet.exits = {'north': home}
attic.exits = {'down': home}
backyard.exits = {'west': home, 'east': creepyforest}
creepyforest.exits = {'west': backyard}
frontyard.exits = {'east': home, 'west': forest}
forest.exits = {'east': frontyard}
