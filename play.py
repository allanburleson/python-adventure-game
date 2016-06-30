#!/usr/bin/python3
import readline
import random
import shelve
import sys

from src import parser
from src import locations
from src import classes

player = classes.Player(locations, locations.start)
previousNoun = ''
turns = 0
while True:
    try:
        command = parser.parseCommand(input('> '))
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
                commandResult = getattr(player, action)(action, noun, 
                                                        hasNoun)
            except AttributeError:
                print('You can\'t do that here.')
            if noun is not None:
                previousNoun = noun
            else:
                previousNoun = ''
            turns += 1
    except KeyboardInterrupt:
        player.die()
