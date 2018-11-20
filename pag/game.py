"""The main game script."""

import os
import shelve
if os.name != "nt":
    import readline


from pag import cwd
from pag import sf_name
from pag.classes import Player
from pag import parser


class Game(object):
    def __init__(self, locations=[], words=None):
        if words:
            for i in words:
                assert i == 'nouns' or i == 'verbs' or i == 'directions' or i == 'extras', 'Bad word input.'
        self._locations = locations
        self._player = None

    def play(self):
        sf_exists = False
        for i in os.listdir(cwd):
            if i.startswith(sf_name):
                sf_exists = True
                break
        if sf_exists:
            save = shelve.open(f'{cwd}/{sf_name}')
            self._player = save['player']
            locations = save['locations']
            save.close()
            self._player.locations = locations
            for i in locations:
                self._player.visited_places[i] = False
            self._player.location.give_info(True, self._player.has_light)
        else:
            self._player = Player(self._locations,
                                  self._start_location())
        previous_noun = ''
        turns = 0
        dark_turn = 0

        # Main game loop
        while True:
            try:
                command = parser.parse_command(input('> '))
                if command is not None:
                    action = command[0]
                    if len(command) >= 2:
                        noun = command[1]
                    else:
                        noun = ''
                    if action is None and noun != '':
                        action = 'go'
                    if previous_noun != '' and noun == 'it':
                        noun = previous_noun
                    # Where game executes result.
                    # Player stuff happens here
                    # Ex: getattr(self._player, "go")(action, noun) -> self._player.go(action, noun)
                    try:
                        result = getattr(self._player, action)(action, noun)
                    except AttributeError:
                        print('This cannot be done.')
                    # Add 1 to player moves if function returns True
                    if result:
                        self._player.moves += 1

                    if noun != '':
                        previous_noun = noun
                    else:
                        previous_noun = ''
                    if self._player.location.dark and not self._player.has_light:
                        if dark_turn < turns:
                            print('A grue magically appeared. However, since '
                                  'this isn\'t Zork, the grue didn\'t eat you;'
                                  ' it just killed you instead. So that\'s alr'
                                  'ight.')
                            self._player.die()
                        else:
                            dark_turn = turns
                    turns += 1
                    if not self._player.location.dark or self._player.has_light:
                        dark_turn = turns
            except KeyboardInterrupt:
                self._player.quit('', '')

    def _start_location(self):
        for loc in self._locations:
            if loc.start:
                return loc
        assert False, 'No location is marked as the start location.'
