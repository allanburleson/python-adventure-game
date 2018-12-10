"""The main game script."""

import os
machine = os.uname().machine
import shelve
import traceback
if os.name != "nt" and not 'iPhone' in machine and not 'iPad' in machine:
    import readline


from pag import cwd
from pag import sf_name
from pag.classes import Player

from pag.interfaces import CommandLineInterface




class GameWorld(object):
    def __init__(self, locations=[], words=None):
        if words:
            for i in words:
                assert i == 'nouns' or i == 'verbs' or i == 'directions' or i == 'extras', 'Bad word input.'
        self._locations = locations
        self._player = None

        self._previous_noun = ''
        self._turns = 0
        self._dark_turn = 0

    def load_player(self, ui):
        sf_exists = False
        for i in os.listdir(cwd):
            if i.startswith(sf_name):
                sf_exists = True
                break
        if sf_exists:
            player = None
            locations = None

            save = shelve.open(f'{cwd}/{sf_name}')

            try:
                player = save['player']
            except Exception:
                pass

            try:
                locations = save['locations']
            except Exception:
                pass

            save.close()

            if player is None or locations is None:
                # Failed loading game.
                self._player = Player(self._locations,
                                      self._start_location(),
                                      ui)
                return

            player.set_ui(ui)
            self._player = player
            self._player.locations = locations
            for i in locations:
                self._player.visited_places[i] = False
            self._player.location.give_info(True, self._player.has_light)
        else:
            self._player = Player(self._locations,
                                  self._start_location(),
                                  ui)


    def game_turn(self, command):
        """
        Take one game turn.
        """
        if command is None:
            return

        action = command[0]
        if len(command) >= 2:
            noun = command[1]
        else:
            noun = ''
        if action is None and noun != '':
            action = 'go'
        if self._previous_noun != '' and noun == 'it':
            noun = self._previous_noun
        # Where game executes result.
        # Player stuff happens here
        # Ex: getattr(self._player, "go")(action, noun) -> self._player.go(action, noun)
        result = False
        try:
            result = getattr(self._player, action)(action, noun)
        except AttributeError as ex:
            # traceback.print_exc()
            print("You cannot do %s." % (action))
        # Add 1 to player moves if function returns True
        if result:
            self._player.moves += 1

        if noun != '':
            self._previous_noun = noun
        else:
            self._previous_noun = ''
        if self._player.location.dark and not self._player.has_light:
            if self._dark_turn < self._turns:
                print('A grue magically appeared. However, since '
                      'this isn\'t Zork, the grue didn\'t eat you;'
                      ' it just killed you instead. So that\'s alr'
                      'ight.')
                self._player.die()
            else:
                self._dark_turn = self._turns
        self._turns += 1
        if not self._player.location.dark or self._player.has_light:
            self._dark_turn = self._turns


    def _start_location(self):
        """
        Return map start location.
        """
        for loc in self._locations:
            if loc.start:
                return loc
        assert False, 'No location is marked as the start location.'

    def quit(self):
        self._player.quit('', '')
