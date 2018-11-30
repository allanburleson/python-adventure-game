

from pag import parser

class SilentUI(object):

    def __init__(self):
        """
        Silent UI for testing.
        """
        pass

    def print(self, output):
        """
        Silent output.
        """
        pass

    def input(self, prompt):
        raise Exception("Silent prompt can not return input.")

class CommandLineInterface(object):
    def __init__(self, world):
        """
        Command line interface
        """
        self._world = world

    def play(self):
        self._world.load_player(self)

        # Main game loop
        while True:
            try:
                command = parser.parse_command(input('> '))
                self._world.game_turn(command)
            except KeyboardInterrupt:
                self._world.quit()

    def print(self, *args, **kwargs):
        print(*args, **kwargs)

    def input(self, prompt):
        return input(prompt)
