#!/usr/local/bin/python3.5
import os
import readline
import shelve
import sys

assert sys.version_info >= (3,5), 'You must use at least Python 3.5.'

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
darkTurn = 0
while True:
    try:
        command = parser.parseCommand(input('> '))
        if command is not None:
            action = command[0]
            if len(command) >= 2:
                noun = command[1]
            else:
                noun = ''
            if action is None and noun != '':
                action = 'go'
            if previousNoun != '' and noun == 'it':
                noun = previousNoun
            try:
                commandResult = getattr(player, action)(action, noun)
            except AttributeError:
                print('You can\'t do that here.')
            if noun != '':
                previousNoun = noun
            else:
                previousNoun = ''
            if player.location.dark and not player.light:
                if darkTurn < turns:
                    print('A grue magically appeared. However, since '\
                          'this isn\'t Zork, the grue didn\'t eat you;'\
                          ' it just killed you instead. So that\'s alr'\
                          'ight.')
                    player.die()
                else:
                    darkTurn = turns
            turns += 1
            if not player.location.dark or player.light:
                darkTurn = turns
    except KeyboardInterrupt:
        player.quit('', '')
