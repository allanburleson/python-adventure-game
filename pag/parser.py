"""A rather messy way of parsing commands."""

from pag import words as pag_words

class Token:
    T_VERB = 'Verb'
    T_NOUN = 'Noun'
    T_EXTRA = 'Extra'
    T_DIRECTION = 'Direction'

    def __init__(self, tvalue, ttype=T_VERB):
        """
        tvalue : Token literal value.
        ttype : Token type.
        """
        self._ttype = ttype
        self._tvalue = tvalue

    def __str__(self):
        return self._tvalue

    def __repr__(self):
        return "{0}<{1}>".format(self._ttype, self._tvalue)

    def __eq__(self, other):
        return other._ttype == self._ttype and other._tvalue == self._tvalue


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

        Returns a sequence of string words
        """

        # Normalise whitespaces
        toreturn = command.lower().strip()
        if len(toreturn) == 0:
            return ""

        word_seq = toreturn.split()
        word_seq = [w for w in word_seq if len(w) > 0]

        # See if command is only a direction
        for i in self._directions:
            if command.strip() == i:
                # Return Verb, Noun
                word_seq = ["go", i]
            else:
                for syn in self._directions[i]:
                    if command.strip() == syn:
                        word_seq = ["go", i]

        # remove extra words
        removing = [word for word in word_seq if word in self._extras]
        for word in removing:
            word_seq.remove(word)

        return word_seq


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


    def eat_verb(self, word_seq):
        """
        Try to consume a verb from a word sequence.

        On success:
         - Returns a new token of type T_VERB
         - Consumed word removed from word_seq.

        On failure:
         - Returns None
         - word_seq unchanged.
        """

        if len(word_seq) == 0:
            return None

        word = word_seq[0]

        for i in self._verbs:
            if word.strip() == i:
                word_seq.pop(0)
                return Token(i)
            else:
                for syn in self._verbs[i]:
                    if (word.strip() == syn):
                        word_seq.pop(0)
                        return Token(i)

        return None

    def eat_noun(self, word_seq):
        """
        Try to consume a noun from a word sequence.

        On success:
         - Returns a new token of type T_NOUN
         - Consumed word removed from word_seq.

        On failure:
         - Returns None
         - word_seq unchanged.
        """

        if len(word_seq) == 0:
            return None

        # Attempt a greedy eat.
        # I.e. attempt to eat 'toilet paper roll'
        # even if we would succeed at 'toilet paper'
        greedy_seq = self.merge_first_words(word_seq)
        if len(greedy_seq) != len(word_seq):
            greedy_res = self.eat_noun(greedy_seq)
            if greedy_res is not None:
                while len(greedy_seq) < len(word_seq):
                    word_seq.pop(0)

                return greedy_res

        word = word_seq[0]

        for i in {**self._nouns, **self._directions}:
            if word == i:
                word_seq.pop(0)
                return Token(i, Token.T_NOUN)

            else:
                for syn in {**self._nouns, **self._directions}[i]:
                    if word == syn:
                        word_seq.pop(0)
                        return Token(i, Token.T_NOUN)


    def merge_first_words(self, word_seq):
        """
        Merge first two words in a word sequence.

        Needed for multi-word words, i.e. 'look at', 'toilet paper'
        """
        if len(word_seq) > 1:
            return [word_seq[0] + " " + word_seq[1]] + word_seq[2:]

        return word_seq[:]

    def parse(self, command):


        prep = Preprocessor()
        prep.supplement_words(self._words)

        word_seq = prep.prep(command)

        parsed_command = []
        # command must start with a verb
        verb = self.eat_verb(word_seq)

        if verb is None and len(word_seq) > 1:
            # Try again, but with multi-word commands. I.e. 'pick up'
            word_seq = self.merge_first_words(word_seq)
            verb = self.eat_verb(word_seq)

        if verb is not None:
            parsed_command.append(verb)
        else:
            print('What?')
            return

        # Next is a noun. Maybe.
        if len(word_seq) > 0:
            noun_result = self.eat_noun(word_seq)

            if noun_result is not None:
                parsed_command.append(noun_result)
            else:
                rest_of_command = " ".join(word_seq)
                print(f'I don\'t understand the noun "{rest_of_command}".')
                return

        if len(word_seq) > 0:
            rest_of_command = " ".join(word_seq)
            print(f'I don\'t understand the extra word "{rest_of_command}".')
            return

        return parsed_command



def parse_command(command, words=None):

    parser = Parser()
    parser.supplement_words(words)
    tokens = parser.parse(command)
    if tokens is None:
        return None
    else:
        return [t._tvalue for t in tokens]
