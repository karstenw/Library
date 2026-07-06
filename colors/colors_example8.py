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

import pdb
kwlog = 1
colors = ximport("colors")
# pattern = ximport("pattern")

import linguistics
import FlowerWord
FlowerWord = FlowerWord.FlowerWord

import pattern
import pattern.en
import pattern.en.wordnet
# en = pattern.en
wordnet = pattern.en.wordnet


# WordNet has a set of global categories (or lexnames)
# into which it classifies all words.
# Examples: verb.weather, noun.artifactm nou.animal, ...
lexname_scores = {}

# wordnet.wn._lexnames ???

# pdb.set_trace()

lexnames = list( wordnet.wn._lexnames )
if kwlog and 0:
    print("wordnet.wn._lexnames:")
    pp(lexnames)


nouns = list( wordnet.NOUNS() )
verbs = list( wordnet.VERBS() )
adjectives = list( wordnet.ADJECTIVES() )


for lexname in lexnames: #wordnet.wn.Lexname.dict.keys():
    lexname_scores[lexname] = []

# pdb.set_trace()

# Traverse all colors in the context (blue, green, ...)
for clr in colors.context: #.keys():
    if kwlog:
        print( "clr:", clr )
        
    # Each color has associated tags: blue -> air, cold, calm, ...
    # Calculate the weight of each tag,
    # if there os a total of 100 tags each weighs 0.01,
    # if there are 20 tags each weighs 0.05, etc. 
    weight = 1.0 / len(colors.context[clr])

    # Each tag will obviously appear in the WordNet dictionary,
    # therefore it will also be classified in a lexname category.
    # Count the number of tags in each lexname category.
    count = {}
    # pdb.set_trace()
    for tag in colors.context[clr]:
        # list(wordnet.NOUNS())
        # list(wordnet.VERBS())
        
        # pdb.set_trace()
        
        fw = FlowerWord( tag )
        synsets = fw.synsets #( tag )
        if not synsets:
            if kwlog:
                print("NO SYNSETS for:", tag )
            continue
        
        # pdb.set_trace()
        for synset in synsets:
            lexname = synset.lexname
            pos = synset.pos
            #print("    lexname:", lexname)
            if not lexname in count:
                count[lexname] = 0.0
            count[lexname] += weight

    #print("count:")
    #pp(count)
    
    # Each lexname then points to a list of colors
    # that have tags categorized under this lexname,
    # together with the tag score from the count dict.
    # noun.feeling -> (blue, 0.09)
    for lexname in count:
        if not lexname in lexname_scores:
            lexname_scores[lexname] = []
        lexname_scores[lexname].append( (clr, count[lexname]) )

# pdb.set_trace()

# So now each lexname in the scores dict points to a number of (color, weight) tuples.
# We normalize the weight so their total weight is 1.0.
# So now we have a percentage of each color's importance for the lexname.
# verb.weather -> grey 24%, orange 19%, white 57%
for lexname in lexname_scores: #.keys():
    s = sum([weight for clr, weight in lexname_scores[lexname]])
    normalized = [(clr, weight/s) for clr, weight in lexname_scores[lexname]]
    lexname_scores[lexname] = normalized

# pdb.set_trace()

# This prints out the full list of colors scores per lexname category.
# pp(lexname_scores)

q = "rabbit" # try out: rave, keyboard, love

for q,x,y in (
    ("rabbit",   150, 150),
    ("rave",     320, 150),
    ("keyboard", 490, 150),
    ("love",     150, 320),
    # ("yearn",    300, 300), # not found
    ("yarn",     320, 320),
    ("rocket",   490, 320),
    ):

    # Now we can do some guessing!
    # If we supply "fox" as a query, we can find out that fox is an animal.
    # Since we have color scores for noun.animal, these might also apply to foxes.

    # use wordnet.synset.lexname()
    l = ""
    fw = FlowerWord( q )
    synsets = fw.synsets
    synset = fw.synset
    # synset = wordnet.synsets( q )
    if synset:
        lexname = synset.lexname
        
        if q in nouns: #  en.is_noun(q):
            l = lexname
        elif q in verbs: #en.is_verb(q): 
            l = "verb." + lexname
        elif q in adjectives: #en.is_adjective(q): 
            l = "adj." + lexname
    if kwlog:
        print( q, "is-a", l )

    clrs = colors.list()
    if l:
        for clr, weight in lexname_scores[l]:
            for i in range(int(weight*100)):
                clrs += colors.color(clr)
        fill(0.5)
        fontsize(14)
        text(q, x-20, y-80 )
        clrs.swarm(x, y, 50)
