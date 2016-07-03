#!/usr/bin/python3
import os
import readline
import shelve

# Change directory to directory that includes play.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from src import parser
from src import locations
from src import classes

try:
    save = shelve.open('save')
    player = save['player']
    Locations = save['locations']
    save.close()
    player.locations = Locations
    for i in Locations:
        player.visitedPlaces[i] = False
    player.location.giveInfo(True)
except:
    player = classes.Player(locations.Location_Storage, locations.start)
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
