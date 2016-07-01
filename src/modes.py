from src import classes


class Mode(object):
    """The Mode class. Define mode and give it a name
        Generic mode handling is defined here. """

    def __init__(self, name):
        super(Mode, self).__init__()


class Combat(Mode):
    """Documentation for Combat"""

    def __init__(self, hp, creatures):
        self.hp = hp
        self.creatures = creatures

    def pStart(self):
        print("You encountered a {0}".format(self.creatures))


a = Combat(5, "apple")


def SwitchMode(mode):
    """Switch mode to 'mode'"""
    mode.pStart()

SwitchMode(a)
