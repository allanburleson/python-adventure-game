

from pag import parser

class SilentUI(object):

    def __init__(self):
        """
        Silent UI for testing.
        """
        pass

class CommandLineInterface(object):
    def __init__(self, world):
        """
        Command line interface
        """
        self._world = world

    def play(self):
        self._world.load_player()

        # Main game loop
        while True:
            try:
                command = parser.parse_command(input('> '))
                self._world.game_turn(command)
            except KeyboardInterrupt:
                self._world.quit()
