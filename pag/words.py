"""Get words from files in "src/dictionary/"."""

import os

def get_word_list(filepath):
    """
    Get a list of words from a file.
    
    Input: file name
    Output: dict with formula {word: [synonym, synonym]}"""
    filepath = os.path.abspath(filepath)
    assert os.path.isfile(filepath), 'Must be a file'
    f = open(filepath, 'r')
    contents = f.read()
    txt = contents.strip().split('\n')
    ntxt = txt[:]
    for line in txt:
        if line[0] == '#':
            ntxt.remove(ntxt[ntxt.index(line)])
        elif ':' not in line:
            ntxt[ntxt.index(line)] = line + ':'
    txt = ntxt
    words = {}
    for line in txt:
        index = line.split(':')[0]
        words[index] = line.split(':')[1].split(',')
        for syn in words[index]:
            if syn == '':
                words[index].remove(syn)
    f.close()
    return words

verbs = get_word_list('dictionary/verbs.txt')
nouns = get_word_list('dictionary/nouns.txt')
extras = get_word_list('dictionary/extras.txt')
directions = get_word_list('dictionary/directions.txt')
