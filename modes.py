# Note: this currently does nothing.
class Mode(object):
    """Documentation for Mode

    """
    def __init__(self, name):
        super(Mode, self).__init__()
        self.name = name


class Combat(Mode):
    """Documentation for Combat"""
    def __init__(self, hp, creatures):
        self.hp = hp
        self.creatures = creatures

    def init(self):
        print("You encountered a {0}".format(self.creature))
    
