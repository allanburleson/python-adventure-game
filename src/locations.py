from src.classes import *

bathroom = Location('Bathroom', [ToiletPaper()], [], showNameWhenExit=True)
bathroom.description = 'There is a toilet and a sink here. They seem'\
                       ' out of place since this is 600 B.C.'
home = Location('Home', [Paper()], [], showNameWhenExit=True)
home.items[0].description = '''"NOTICE:
All able-bodied individuals are asked to assist in capturing or
destroying the Robots of Unusual Size. More commonly knows as ROUS, they
have been terrorizing humankind for several weeks and already 3000 lives
have been lost. Visit our headquarters to register and get free 
ROUS-fighting supplies.

Here is what popular media outlets have to say about this menace:
'Robots of Unusual Size? I don't think they exist.'--DPR Daily

'Well, since the population of the universe is zero, I'm not sure how
this issue came about. (See Guide chapter 5) Hopefully this will be 
resolved.'--Zarniwoop, HG2G

'We extend condolences to all whose friends and family have been harmed
in these attacks. Many thanks to the RRO which so dilligently protects
our loved ones.'--Old York Times

Please await further letters for updates.

--RRO (ROUS Resistance Organization)"

Written under this letter is a handwritten note that says:
"RRO headquarters: sssessw"'''
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
