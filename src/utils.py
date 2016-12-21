"""An assortment of different useful functions."""

import os

def inInventory(itemClass, player):
    for item in player.inventory:
        if isinstance(item, itemClass):
            return True
    return False


def getItemFromName(itemName, itemList, player):
    """Retrieve an item's object from its name."""
    for item in itemList:
        if itemName == item.name:
            return item
    return False


def getIndefArticle(noun):
    """Get the indefinite article that precedes a noun."""
    vowels = [i for i in 'aeiou']
    consonants = [i for i in 'bcdfghjklmnpqrstvwxyz1234567890']
    if noun[0] in vowels:
        return 'an'
    elif noun[0] in consonants:
        return 'a'


def clrscn():
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")


def numberStrings(*strings):
    """Print a list of strings with a number preceding each."""
    for number, string in enumerate(strings):
        number += 1
        print(number, string)
    return

