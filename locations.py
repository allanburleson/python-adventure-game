from classes import *

test = Location('Test', [], [])
test.description = 'This is a test location.'
home = Location('Home', [], [], {'north': test})
home.description = 'You are in a familiar cabin made out of logs. '\
                   'There is a pleasantly warm fire in the fireplace '\
                   'and a comfortable-looking armchair beside it.'
start = Location('Start', [Mirror()], [])
start.description = 'You are in a small room with concrete walls and '\
                    'no windows.'
