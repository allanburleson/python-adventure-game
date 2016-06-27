import readline
import random
import shelve
import time

from objects import *
from parser import *

def inInventory(item):
    for item in player.inventory:
        if noun == item.name:
            return True
            break
    return False
    
    
def getItemFromName(itemName, itemList):
    for item in itemList:
        if itemName == item.name:
            return item
    return False
    
    
def specialCommands(action, noun):
    if player.location == start:
        if action == 'use' and noun == 'magic mirror' and magicMirror in player.inventory:
            print('The mirror exploded. A large shard of glass hit you in the face.')
            player.die()
        elif action == 'break' and noun == 'magic mirror' and (magicMirror in player.location.items or magicMirror in player.inventory):
            print('You smashed the mirror, which happened to be the only thing holding the space-time continuum together.')
            player.die()
    

previousNoun = ''
while True:
    command = parseCommand(input('> '))
    if command is not None:
        hasNoun = True
        action = command[0]
        if len(command) >= 2:
            noun = command[1]
        else:
            hasNoun = False
            noun = None
        if previousNoun != '' and noun == 'it':
            noun = previousNoun
        specialCommands(action, noun)
        if action == 'look':
            if not hasNoun or noun == 'around':
                player.location.look()
            else:
                item = getItemFromName(noun, player.inventory)
                if item:
                    item.examine()
                else:
                    print('You do not have {0}'.format(noun))
        elif action == 'take':
            if not hasNoun:
                print('What do you want to take?')
            else:
                item = getItemFromName(noun, items)
                if item:
                    player.take(item)
        elif action == 'help':
            print('I can only understand what you say if you first type an action and then a noun (if necessary). My vocabulary is limited.')
        elif action == 'xyzzy' or (action == 'say' and noun == 'xyzzy'):
            if magicMirror in player.inventory:
                if player.location == start:
                    player.score += 1
                print('You vanished and reappeared in your house.\n')
                player.move(home)
            else:
                print('There was a flash of light...and your score was mysteriously lowered by one.')
                player.score -= 1
        elif action == 'quit':
            player.die()
        else:
            print('You can\'t do that here.')
        if noun is not None:
            previousNoun = noun
        else:
            previousNoun = ''