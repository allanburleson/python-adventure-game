from src import classes
import random


class Mode(object):
    """The Mode class. Define mode and give it a name
        Generic mode handling is defined here. """

    def __init__(self, name):
        super(Mode, self).__init__()
        self.name = name


class Rand_Num_Game():
    """Documentation for Rand_Num_Game

    """

    def __init__(self, sides):
        self.sides = sides

    def pStart(self):
        awk = random.randint(0, self.sides)
        print(awk)


def SwitchMode(mode):
    """Switch mode to 'mode'"""
    mode.pStart()
