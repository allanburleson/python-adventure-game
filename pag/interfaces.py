

from pag import parser

### These should both be Interface subclasses or something
class SilentUI(object):

    def __init__(self):
        """
        Silent UI for testing.
        """
        self._prompts = {}
        pass

    def set_reply(self, re_prompt, reply):
        """
        Hard-code prompts and replies.

        Prompt matcher should be a pre-compiled regexp.
        """
        self._prompts[re_prompt] = reply


    def print(self, output):
        """
        Silent output.
        """
        pass

    def input(self, prompt):
        """
        Prompt silent UI for a input response.
        """
        for regexp in self._prompts:
            try:
                res = regexp.match(prompt)
                if res:
                    return self._prompts[regexp]
            except Exception:
                pass

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
