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
closet = Location('Closet', [], [], showNameWhenExit=True)
closet.description = 'You are in a closet that is full of cobwebs.'
yard = Location('Yard', [], [Snail()])
yard.description = 'You are in the yard of your house.'
creepyforest = Location('Creepy forest', [], [Ghost()], showNameWhenExit=True)
creepyforest.description = 'You are in a spooky forest. '\
                           'How are you in the middle of a large fores'\
                           't? Don\'t ask me!'
home.exits = {'north': bathroom, 'south': closet, 'east': yard}
bathroom.exits = {'south': home}
closet.exits = {'north': home}
yard.exits = {'west': home, 'east': creepyforest}
