#!/usr/bin/env python3
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
    """ Main Game Loop. """
    utils.clrscn()

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
        player.location.giveInfo(True, player.hasLight)
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
                # Where game executes result.
                #try:
                    # Player stuff happens here
                    # Ex: getattr(player, "go")(action, noun) -> player.go(action, noun)
                commandResult = getattr(player, action)(action, noun)
                #except AttributeError:
                #    print('You can\'t do that here.')

                if noun != '':
                    previousNoun = noun
                else:
                    previousNoun = ''
                if player.location.dark and not player.hasLight:
                    if darkTurn < turns:
                        print('A grue magically appeared. However, since '
                              'this isn\'t Zork, the grue didn\'t eat you;'
                              ' it just killed you instead. So that\'s alr'
                              'ight.')
                        player.die()
                    else:
                        darkTurn = turns
                turns += 1
                if not player.location.dark or player.hasLight:
                    darkTurn = turns
        except KeyboardInterrupt:
            player.quit('', '')

# Run.
if __name__ == '__main__':
    main()
