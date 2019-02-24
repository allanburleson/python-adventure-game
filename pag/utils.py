"""An assortment of different useful functions."""

import os


def get_item_from_name(item_name, item_list):
    """Retrieve an item's object from its name."""
    ### Potential issue if multiple items share a name
    for item in item_list:
        if item_name == item.name:
            return item
    return None


def get_indef_article(noun):
    """Get the indefinite article that precedes a noun."""
    ### You can use strings library
    vowels = [i for i in 'aeiou']
    consonants = [i for i in 'bcdfghjklmnpqrstvwxyz1234567890']
    if noun[0] in vowels:
        return 'an'
    elif noun[0] in consonants:
        return 'a'


def clrscn():
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")


def number_strings(*strings):
    """Print a list of strings with a number preceding each."""
    for number, string in enumerate(strings):
        number += 1
        print(number, string)
    return
