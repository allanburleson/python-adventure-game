import os

cwd = os.getcwd()
# Change directory to directory that includes play.py
os.chdir(os.path.dirname(os.path.abspath(__file__))) ### Is this necessary?
sf_name = '.pag-save' ### Base savefile name on game name so there aren't conflicts


from pag.game import GameWorld
from pag.interfaces import CommandLineInterface
