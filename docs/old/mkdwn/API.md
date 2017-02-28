# Table of Contents



# Basic Usage

## Items

### What are Items?

Items are a class which have:

- a name

- a description that is shown when examining the item

- a local description that is shown when looking at the room.

Items also have a method ```examine``` used to print the description

### Creating Items

To create an Item, it must be a subclass of class Item.

Then, you must use super().__init__('attrs'),
to change the attributes of the item.

Example:
```
class ITEM_NAME(Item):
   def __init__(self):
      super().__init__(name="ITEM NAME"
                       description="ITEM DESCRIPTION"
                       locDescription="LOCAL ITEM DESCRIPTION")
```

## Creatures

### What are Creatures?

A Creature is a class which has:

- A name

- A description

- And an hp stat.

It also has a method ```describe``` which allows its description to be printed.

### Creating Creatures

Creatures are not directly created.

Instead, it is used as a superclass of another class.

The various creatures are:

Baddie - Used to define a Creature that is harmful to the player.

#### Spawning Baddies

"Baddies" are spawned trough defining a class, then making it a subclass of "Baddie"

Then, each attribute is changed through changing the attributes of the superclass

Example:
```
class BADDIE_NAME(Baddie):
   def __init__(self):
      super().__init__(name='BADDIE NAME',
                       hp=BADDIE_HP
                       description='BADDIE DESCRIPTION'
                       power=BADDIE_POWER)
```

## Locations

### What is a location?

A location is a class defined in classes.py

A location has the following attributes:

- A name

- Any items 

- Any creatures

- Any exits

- If the player can use 'back' to return to that room

- If it's dark or not

- If the room name should be shown when exiting

- And a description

Items and Creatures are kept in a list, and must be called instead of putting their descriptions.

Likewise, any exits must be defined with: 
{'DIRECTION': ROOM }

### Creating a room

A room is created by making an instance of the "Location" class.

The attributes that a room has are as follows:

ROOM_VAR = Location("ROOM NAME", [ITEMS], [CREATURES], {EXITS}, "DESCRIPTION")

Example:
```
test = Location("Test", [ITEM_NAME()], [BADDIE_NAME()], {"north": EXIT_ROOM})

# Usually, the description is done later.

test.description = "ROOM_DESCRIPTION"
```

