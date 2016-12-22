import os

cwd = os.getcwd()
# Change directory to directory that includes play.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sf_name = '.pag-save'


from pag.game import Game
