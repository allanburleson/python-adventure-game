from classes import *

magicMirror = Item('magic mirror')
magicMirror.description = \
    'The mirror is round and you can see your reflection clearly. Under the glass is an inscription that says "XYZZY."'
magicMirror.locDescription = 'There is a small mirror lying on the ground.'
orc = Creature('orc')
orc.description = 'There is a nasty-looking orc in the room.'
start = Location('Start', [magicMirror], [])
start.description = 'You are in a small room with concrete walls and no windows.'
test = Location('Test', [], [])
test.description = 'This is a test location.'
home = Location('Home', [], [], {'north': test})
home.description = 'You are in a familiar cabin made out of logs. There is a pleasantly warm fire in the fireplace and a comfortable-looking armchair beside it.'
player = Player(start)
