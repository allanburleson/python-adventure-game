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
