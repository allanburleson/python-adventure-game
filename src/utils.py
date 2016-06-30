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
    if noun[0] in 'a e i o u'.split(' '):
        return 'an'
    elif noun[0] in 'b c d f g h j k l m n p q r s t v w x y z 1 2 3 4'\
                    '5 6 7 8 9 0'.split(' '):
        return 'a'
