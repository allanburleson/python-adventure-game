import readline
import random
import shelve

from parser import *
from locations import *

player = Player(locations, start)
previousNoun = ''
while True:
    command = parseCommand(input('> '))
    if command is not None:
        hasNoun = True
        action = command[0]
        if len(command) >= 2:
            noun = command[1]
        else:
            hasNoun = False
            noun = None
        if previousNoun != '' and noun == 'it':
            noun = previousNoun
        try:
            commandResult = getattr(player, action)(action, noun, hasNoun)
        except AttributeError:
            print('You can\'t do that here.')
        if noun is not None:
            previousNoun = noun
        else:
            previousNoun = ''
