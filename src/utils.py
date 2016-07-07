import os

vowels = ['a e i o u']
constanents = ['b c d f g h j k l m n p q r s t v w x y z 1 2 3 4 \
                5 6 7 8 9 0']


def inInventory(itemClass, player):
    for item in player.inventory:
        if isinstance(item, itemClass):
            return True
            break
    return False


def getItemFromName(itemName, itemList, player):
    for item in itemList:
        if itemName == item.name:
            return item
    return False


def getIndefArticle(noun):
    if noun[0] in vowels.split(' '):
        return 'an'
    elif noun[0] in constanents.split(' '):
        return 'a'


def clrscn():
    os.system("cls" if os.name == "nt" else "clear")
