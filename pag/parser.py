"""A rather messy way of parsing commands."""

from pag import words as pag_words

class Preprocessor:
    def __init__(self):

        self._directions = pag_words.directions
        self._extras = pag_words.extras


    def supplement_words(self, words=None):
        """
        """
        if words is not None:

            if 'extras' in words:
                self._extras = {**self._extras, **words['extras']}

            if 'directions' in words:
                self._directions = {**self._verbs, **words['directions']}


    def prep(self, command):
        """
        Pre-process a command.
        """

        # Normalise whitespaces
        toreturn = command.lower().strip()
        if len(toreturn) == 0:
            return ""

        tokens = toreturn.split()
        tokens = [t for t in tokens if len(t) > 0]

        # See if command is only a direction
        for i in self._directions:
            if command.strip() == i:
                # Return Verb, Noun
                tokens = ["go", i]
            else:
                for syn in self._directions[i]:
                    if command.strip() == syn:
                        tokens = ["go", i]

        # remove extra words
        removing = [word for word in tokens if word in self._extras]
        for word in removing:
            tokens.remove(word)
        toreturn = ' '.join(tokens)

        return toreturn


class Parser:
    def __init__(self):
        pass
        self._words = None
        self._verbs = pag_words.verbs
        self._nouns = pag_words.nouns
        self._extras = pag_words.extras
        self._directions = pag_words.directions


    def supplement_words(self, words=None):
        """
        """

        self._words = words

        if words is not None:
            if 'verbs' in words:
                self._verbs = {**self._verbs, **words['verbs']}

            if 'nouns' in words:
                self._nouns = {**self._nouns, **words['nouns']}

            if 'extras' in words:
                self._extras = {**self._extras, **words['extras']}

            if 'directions' in words:
                self._directions = {**self._verbs, **words['directions']}


    def eat_verb(self, command):
        """
        Try to consume a verb.
        """
        verb = ''
        typed_verb = ''
        for i in self._verbs:
            if command.startswith(i + ' ') or command.strip() == i:
                verb = i
                typed_verb = i
            if command.strip() == i:
                expect_noun = False
            else:
                for syn in self._verbs[i]:
                    if (command.startswith(syn + ' ') or
                        command.strip() == syn):
                        verb = i
                        typed_verb = syn
                    if command.strip() == syn:
                        expect_noun = False

        return verb, typed_verb

    def eat_noun(self, command, typed_verb):
        """
        Try to consume a noun.
        """
        rest_of_command = command.split(typed_verb + ' ')[1]
        for i in {**self._nouns, **self._directions}:
            if rest_of_command == i:
                noun = i
                return noun

            else:
                for syn in {**self._nouns, **self._directions}[i]:
                    if rest_of_command == syn:
                        noun = i
                        return noun

    def parse(self, command):


        prep = Preprocessor()
        prep.supplement_words(self._words)

        command = prep.prep(command)

        parsed_command = []
        # command must start with a verb
        verb, typed_verb = self.eat_verb(command)
        if verb != '':
            parsed_command.append(verb)
        else:
            print('What?')
            return

        # next is a noun
        rest_of_command = ''
        if len(command) > len(typed_verb) + 1:
            noun_result = self.eat_noun(command, typed_verb)
            if noun_result != '' and noun_result is not None:
                parsed_command.append(noun_result)
            else:
                rest_of_command = command.split(typed_verb + ' ')[1]
                print(f'I don\'t understand the noun "{rest_of_command}."')
                return

        return parsed_command



def parse_command(command, words=None):

    parser = Parser()
    parser.supplement_words(words)
    return parser.parse(command)
