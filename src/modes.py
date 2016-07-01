from src import classes


class Mode(object):
    """The Mode class. Define mode and give it a name
        Generic mode handling is defined here. """

    def __init__(self, name):
        super(Mode, self).__init__()
        self.name = name


def Callm(mode):
    """Switch mode to 'mode'"""
    mode.pStart()
