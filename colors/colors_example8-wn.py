# INFERENCE FUN!
# Categorize the tags associated to each color in the context.
# Keep a score how much each color is present in a category.
# Find out the category of a given search word.
# Since the word is part of the category,
# the infered color for that category should apply to the word.

import os
import sys
import pprint
pp=pprint.pprint

colors = ximport("colors")
# pattern = ximport("pattern")

import linguistics
import wn


import pdb

# WordNet has a set of global categories (or lexnames)
# into which it classifies all words.
# Examples: verb.weather, noun.artifactm nou.animal, ...
lexname_scores = {}

# wordnet.wn._lexnames ???

# lexnames = list( wordnet.wn._lexnames )
# pp(lexnames)

nouns = []
verbs = []
adjectives = []
for word in wn.words(lang="en"):
    if word.pos == 'n':
        nouns.append( word )
    elif word.pos == 'v':
        verbs.append( word )
    elif word.pos == 'a':
        adjectives.append( word )


for lexname in lexnames: #wordnet.wn.Lexname.dict.keys():
    lexname_scores[lexname] = []

# pdb.set_trace()

# Traverse all colors in the context (blue, green, ...)
for clr in colors.context.keys():
    print( clr )
    
    colorcontext = colors.context[clr]

    # Each color has associated tags: blue -> air, cold, calm, ...
    # Calculate the weight of each tag,
    # if there os a total of 100 tags each weighs 0.01,
    # if there are 20 tags each weighs 0.05, etc. 
    weight = 1.0 / len( colorcontext )

    # Each tag will obviously appear in the WordNet dictionary,
    # therefore it will also be classified in a lexname category.
    # Count the number of tags in each lexname category.
    count = {}
    for tag in colorcontext:
        # list(wordnet.NOUNS())
        # list(wordnet.VERBS())
        
        synsets = wordnet.synsets( tag )
        if not synsets:
            continue
        synsets = [ synsets[0] ]
        # print("tag:", tag)
        # synset = synsets[0]
        for synset in synsets:
            lexname = synset.lexname
            pos = synset.pos
            #print("    lexname:", lexname)
            if not lexname in count:
                count[lexname] = 0.0
            count[lexname] += weight

    # print("count:")
    # pp(count)
    # Each lexname then points to a list of colors
    # that have tags categorized under this lexname,
    # together with the tag score from the count dict.
    # noun.feeling -> (blue, 0.09)
    for lexname in count:
        if not lexname in lexname_scores:
            lexname_scores[lexname] = []
        lexname_scores[lexname].append( (clr, count[lexname]) )

# pdb.set_trace()
# pp( lexname_scores )

# So now each lexname in the scores dict points to a number of (color, weight) tuples.
# We normalize the weight so their total weight is 1.0.
# So now we have a percentage of each color's importance for the lexname.
# verb.weather -> grey 24%, orange 19%, white 57%
for lexname in lexname_scores.keys():
    s = sum([weight for clr, weight in lexname_scores[lexname]])
    normalized = [(clr, weight/s) for clr, weight in lexname_scores[lexname]]
    lexname_scores[lexname] = normalized

# This prints out the full list of colors scores per lexname category.
# pp(lexname_scores)

q = "rabbit" # try out: rave, keyboard, love

for q,x,y in (
    ("rabbit",   100, 100),
    ("rave",     300, 100),
    ("keyboard", 100, 300),
    ("love",     300, 300),
    ("yearn",    100, 500),
    ):

    # Now we can do some guessing!
    # If we supply "fox" as a query, we can find out that fox is an animal.
    # Since we have color scores for noun.animal, these might also apply to foxes.

    # use wordnet.synset.lexname()
    l = ""
    #if q == 'yearn':
    #    pdb.set_trace()
    synsets = wordnet.synsets( q )
    if synsets:
        synset = synsets[0]
        lexname = synset.lexname

        if q in nouns: #  en.is_noun(q):
            l = lexname
            #synset = wordnet.synsets( q )[0]
            #l = synset.lexname
            # l = "noun."+en.noun.lexname(q)
        elif q in verbs: #en.is_verb(q): 
            #l = "verb."+en.verb.lexname(q)
            #synset = wordnet.synsets( q )[0]
            l = "verb." + lexname
        elif q in adjectives: #en.is_adjective(q): 
            # l = "adj."+en.adjective.lexname(q)
            #synset = wordnet.synsets( q )[0]
            # l = "adj." + synset.lexname
            l = "adj." + lexname

        print( q, "is-a", l )

        clrs = colors.list()
        for clr, weight in lexname_scores[l]:
            for i in range(int(weight*100)):
                clrs += colors.color(clr)

        clrs.swarm(x, y, 50)
