#!/usr/bin/env python3
from pag import Game
from pag.classes import *


class ToiletPaper(Item):
    def __init__(self):
        super().__init__(name='toilet paper',
                         description='The toilet paper is labeled "X-t'
                         'raSoft.',
                         loc_description='A roll of toilet paper is in '
                         'the room.',
                         weight=1)
                         

home = Location('Home', start=True, show_name_when_exit=True)
home.description = 'You\'re at home.'
bathroom = Location('Bathroom', items=[ToiletPaper()], show_name_when_exit=True)
bathroom.description = 'You\'re in the bathroom.'
home.exits = {'south': bathroom}
bathroom.exits = {'north': home}

game = Game(location_list)
game.play()
