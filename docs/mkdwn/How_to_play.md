# How to play

Type commands to make the player do things. Commands should be in very simple English, with a verb first and then a noun if one is needed.

Example: "examine mirror"

Prepositions such as "at" can be used, but the parser just ignores them, so "look at tree" is interpreted the same as "look tree".

Many words have synonyms that the parser treats as the same word, such as monster and beast. If a word doesn't work, try a synonym of the word.

# Commands

## look

The look command prints information about the player's surroundings to the console. Adding a noun to the command will make it describe that item in the player's inventory (if it exists).

Synonyms

- examine

- see

## take

The take command puts the specified item into the player's inventory if that item is in the player's current location.

Synonyms

- pick up

- grab

## drop

The drop command does the opposite of take, removing an item from the player's inventory and adding it to the location.

## quit

The quit command ends the game.

Synonyms

- exit

## help

The help command prints a short help message.

Synonyms

- ?

## go

The go command, when supplied a direction, moves the player in that direction if there is an exit in that direction.

Synonyms

- move

- travel

# More?

There are more commands, but the ones not documented are either hidden or incomplete.
