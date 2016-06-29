from src.words import verbs, nouns, extras


def parseCommand(command):
    command = command.lower()
    # remove extra words
    splitCmd = command.split(' ')
    removing = []
    for word in splitCmd:
        if word in extras:
            removing.append(word)
    for word in removing:
        splitCmd.remove(word)
    command = ' '.join(splitCmd)
    parsedCommand = []
    # command must start with a verb
    noNoun = False
    verb = ''
    typedVerb = ''
    for i in verbs:
        if command.startswith(i + ' ') or command.strip() == i:
            verb = i
            typedVerb = i
        if command.strip() == i:
            noNoun = True
        else:
            for syn in verbs[i]:
                if command.startswith(syn + ' ') or (
                   command.strip() == syn):
                    verb = i
                    typedVerb = syn
                if command.strip() == syn:
                    noNoun = True
    if verb != '':
        parsedCommand.append(verb)
    else:
        print('What?')
        return
    # next is a noun
    noun = ''
    restOfCommand = ''
    if not noNoun:
        if len(command) > len(typedVerb) + 1:
            restOfCommand = command.split(typedVerb + ' ')[1]
            for i in nouns:
                if restOfCommand == i:
                    noun = i
                else:
                    for syn in nouns[i]:
                        if restOfCommand == syn:
                            noun = i
            if noun != '':
                parsedCommand.append(noun)
            else:
                print('I don\'t understand the noun "{0}."'.format(
                                                         restOfCommand))
                return
    return parsedCommand
