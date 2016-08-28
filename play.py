#!/usr/bin/env python3.5
import os
import readline
import shelve
import sys

assert sys.version_info >= (3, 5), 'You must use at least Python 3.5.'

# Change directory to directory that includes play.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Below removes the save file for devel purposes
os.system("rm save.db")

from src import parser
from src import locations
from src import classes
from src import utils


def main():
    stdscn = classes.Screen()
    stdscn.clrscn()

    sfExists = False
    for i in os.listdir():
        if i.startswith('save'):
            sfExists = True
            break
    if sfExists:
        save = shelve.open('save')
        player = save['player']
        Locations = save['locations']
        save.close()
        player.locations = Locations
        for i in Locations:
            player.visitedPlaces[i] = False
        player.location.giveInfo(True, player.light)
    else:
        player = classes.Player(locations.Location_Storage, locations.start)
    previousNoun = ''
    turns = 0
    darkTurn = 0
    # Main game loop
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
                # Where game executes(?) result.
                try:
                    commandResult = getattr(player, action)(action, noun)
                except AttributeError:
                    # Section used for things other than the player.
                    
                    # I'm a bit worried bc this in an AttributeError
                    #  try/except clause and might be nested and
                    #  then this will be a big amalgation and then
                    #  the whole `main`function will be super un-
                    #  portable.
                    try:
                        commandResult = getattr(stdscn, action)()
                    except:
                        print("You can\'t do that here.")
                
                if noun != '':
                    previousNoun = noun
                else:
                    previousNoun = ''
                if player.location.dark and not player.light:
                    if darkTurn < turns:
                        print('A grue magically appeared. However, since '
                              'this isn\'t Zork, the grue didn\'t eat you;'
                              ' it just killed you instead. So that\'s alr'
                              'ight.')
                        player.die()
                    else:
                        darkTurn = turns
                turns += 1
                if not player.location.dark or player.light:
                    darkTurn = turns
        except KeyboardInterrupt:
            player.quit('', '')

# Run.
if __name__ == '__main__':
    main()
