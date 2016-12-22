"""A rather messy way of parsing commands."""

from pag.words import verbs, nouns, extras, directions


def parse_command(command):
    command = command.lower()
    # remove extra words
    split_cmd = command.split(' ')
    removing = [word for word in split_cmd if word in extras]
    for word in removing:
        split_cmd.remove(word)
    command = ' '.join(split_cmd)
    parsed_command = []
    # command must start with a verb
    no_noun = False
    verb = ''
    typed_verb = ''
    for i in verbs:
        if command.startswith(i + ' ') or command.strip() == i:
            verb = i
            typed_verb = i
        if command.strip() == i:
            no_noun = True
        else:
            for syn in verbs[i]:
                if command.startswith(syn + ' ') or (
                   command.strip() == syn):
                    verb = i
                    typed_verb = syn
                if command.strip() == syn:
                    no_noun = True
    if verb != '':
        parsed_command.append(verb)
    else:
        # See if command is only a direction
        for i in directions:
            if command.strip() == i:
                # Return Verb, Noun
                return [None, i]
            else:
                for syn in directions[i]:
                    if command.strip() == syn:
                        return [None, i]
        print('What?')
        return
    # next is a noun
    noun = ''
    rest_of_command = ''
    if not no_noun:
        if len(command) > len(typed_verb) + 1:
            rest_of_command = command.split(typed_verb + ' ')[1]
            for i in {**nouns, **directions}:
                if rest_of_command == i:
                    noun = i
                else:
                    for syn in {**nouns, **directions}[i]:
                        if rest_of_command == syn:
                            noun = i
            if noun != '':
                parsed_command.append(noun)
            else:
                print(f'I don\'t understand the noun "{rest_of_command}."')
                return
    return parsed_command
