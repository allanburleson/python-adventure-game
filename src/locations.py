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
backyard = Location('Backyard', [], [Snail()])
backyard.description = 'You are in the backyard of your house.'
frontyard = Location('Front Yard', [Chest([Sword()], True)], [])
frontyard.description = 'You are in your front yard.'
creepyforest = Location('Creepy forest', [], [Ghost()], showNameWhenExit=True)
creepyforest.description = 'You are in a spooky forest. '\
                           'How are you in the middle of a large fores'\
                           't? Don\'t ask me!'
                           
home.exits = {'north': bathroom, 'south': closet, 'east': backyard,
              'west': frontyard}
bathroom.exits = {'south': home}
closet.exits = {'north': home}
backyard.exits = {'west': home, 'east': creepyforest}
frontyard.exits = {'east': home}
