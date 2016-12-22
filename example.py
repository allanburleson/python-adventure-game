#!/usr/bin/env python3
from pag import Game
from pag import classes

# This gives the Game the list of all locations that is updated every time a
# new location is created. Since setting a variable to another variable with a
# list points to the one list's memory address, the list in the game class also
# updates.
game = Game(locations=classes.location_list)


class ToiletPaper(classes.Item):
    def __init__(self):
        super().__init__(name='toilet paper',
                         description='The toilet paper is labeled "X-t'
                         'raSoft.',
                         loc_description='A roll of toilet paper is in '
                         'the room.',
                         weight=1)


home = classes.Location('Home', start=True, show_name_when_exit=True)
home.description = 'You\'re at home.'
bathroom = classes.Location('Bathroom', items=[ToiletPaper()], show_name_when_exit=True)
bathroom.description = 'You\'re in the bathroom.'
home.exits = {'south': bathroom}
bathroom.exits = {'north': home}

game.play()
