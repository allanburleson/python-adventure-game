from src.classes import *

bathroom = Location('Bathroom', [ToiletPaper(),Sword()], [], showNameWhenExit=True)
bathroom.description = 'There is a toilet and a sink here. They seem'\
                       ' out of place since this is 600 B.C.'
home = Location('Home', [], [], showNameWhenExit=True)
home.description = 'You are in a familiar cabin made out of logs. '\
                   'There is a pleasantly warm fire in the fireplace '\
                   'and a comfortable-looking armchair beside it.'
start = Location('Start', [Mirror()], [])
start.description = 'You are in a small room with concrete walls and '\
                    'no windows.'
closet = Location('Closet', [], [Orc()], showNameWhenExit=True)
closet.description = 'You are in a closet that is full of cobwebs.'
home.exits = {'north': bathroom, 'south': closet}
bathroom.exits = {'south': home}
closet.exits = {'north': home}
