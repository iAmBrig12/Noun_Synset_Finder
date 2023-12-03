################################################################################ 
#
#       AUTHOR: 
#           Brigham Thornock 
#  DESCRIPTION: 
#           Reads in a text file, tokenizes by sentence then words, 
#           then identifies the first noun and displays synsets with definitions.
#
#           Adapted from Human Language Technologies class assignment
# DEPENDENCIES: 
#           Created with Python 3.11.5 
#           re, nltk, wordnet, string
# 
################################################################################

import nltk
import re
from nltk.corpus import wordnet as wn
import string


def divider(text="", char="-", divider_length=80):
    if not (text==""):
        text = ' ' + text + ' '
    print(text.center(divider_length, char))

punct = string.punctuation

with open("text_web.txt", "r") as in_file:
    raw_text = in_file.read()
    raw_text = re.sub('<.*?>', '', raw_text)
    raw_text = re.sub('@@\d{7}', '', raw_text)
    raw_text = raw_text.replace('@', '')
    raw_text = raw_text.strip()

    sent_list = nltk.sent_tokenize(raw_text)

    
    for index, sent in enumerate(sent_list[:100]):
        divider(f'sentence {index}')
        
        word_list = nltk.word_tokenize(sent)
        tagged_words = nltk.pos_tag(word_list)
        print( f'\n{sent}\n\n{tagged_words}\n')

        nouns = [word[0] for word in tagged_words if (word[1].startswith('NN') and word[0] not in punct)]
        
        if not nouns:
            print('\nNO NOUNS FOUND\n\n')
            continue

        noun_syns = []
        for noun in nouns:
            noun_syns.append(wn.synsets(noun, pos='n'))

        print(f'\nFIRST NOUN: {nouns[0]}\n')

        for synset1 in noun_syns[0]:
            print(f'\n{synset1}: {synset1.definition()[:30]}')

            if len(nouns) > 1:
                for index, synsets in enumerate(noun_syns[1:]):
                    if synsets:
                        score = wn.path_similarity(synset1, synsets[0])
                        print(f'\n   {nouns[index+1]}'.ljust(20) + f'similarity: {score}')
                    else:
                        print(f'\n   {nouns[index+1]}'.ljust(20) + 'NOT FOUND IN WORDNET')

            else:
                print('\n   no other nouns in sentence')

        print('\n\n')