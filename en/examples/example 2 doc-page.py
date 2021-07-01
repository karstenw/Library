"""
How to get the library up and running

Put the en library folder in the same folder as your script so NodeBox can find the library. You can also put it in ~/Library/Application Support/NodeBox/. It takes some time to load all the data the first time.
"""

from __future__ import print_function

import pprint
pp = pprint.pprint

en = ximport("en")

"""
Verb conjugation

NodeBox English Linguistics knows the verb tenses for about 10000 English verbs.

The verb.infinitive() command returns the infinitive form of a verb:
"""

print()
print( "Verb infinitive 'swimming':", )
print( en.verb.infinitive("swimming") )
# >>> swim

"""
The verb.present() command returns the present tense for the given person. Known values for person are 1, 2, 3, "1st", "2nd", "3rd", "plural", "*". Just use the one you like most.
"""

print()
print( "Verb present 'gave':", )
print( en.verb.present("gave") )
print( "Verb present 'gave' person=3, negate=False:", )
print( en.verb.present("gave", person=3, negate=False) )
# >>> give
# >>> gives

"""
The verb.present_participle() command returns the present participle tense:
"""

print()
print( "Verb present participle 'be':", )
print( en.verb.present_participle("be") )
# >>> being

"""
Return the past tense:
"""

print()
print( "Verb past 'give':", )
print( en.verb.past("give") )
print( "Verb past 'be' person=1, negate=True:", )
print( en.verb.past("be", person=1, negate=True) )
# >>> gave
# >>> wasn't

"""
Return the past participle tense:
"""

print()
print( "Verb past participle 'be':",  )
print( en.verb.past_participle("be") )
# >>> been

"""
A list of all possible tenses:
"""

print()
print( "Verb tenses:" )
print( en.verb.tenses() )
# >>> ['past', '3rd singular present', 'past participle', 'infinitive', 
# >>>  'present participle', '1st singular present', '1st singular past', 
# >>>  'past plural', '2nd singular present', '2nd singular past', 
# >>>  '3rd singular past', 'present plural']

"""
The verb.tense() command returns the tense of the given verb:
"""

print()
print( "Verb tense 'was':", )
print( en.verb.tense("was") )
# >>> 1st singular past

"""
Return True if the given verb is in the given tense:
"""

print()
print( """Verb is tense "wasn't"  "1st singular past", negated=True:""", )
print( en.verb.is_tense("wasn't", "1st singular past", negated=True) )

print( """Verb is present "does" person=1:""",  )
print( en.verb.is_present("does", person=1) )

print( """Verb is present participle "doing":""",  )
print( en.verb.is_present_participle("doing") )
print( """Verb is past participle "done":""",  )
print( en.verb.is_past_participle("done") )
# >>> True
# >>> False
# >>> True
# >>> True

"""
The verb.is_tense() command also accepts shorthand aliases for tenses: inf, 1sgpres, 2gpres, 3sgpres, pl, prog, 1sgpast, 2sgpast, 3sgpast, pastpl and ppart.
Spelling corrections

NodeBox English Linguistics is able to perform spelling corrections based on Peter Norvig's algorithm. The spelling corrector has an accuracy of about 70%.

The spelling.suggest() returns a list of possible corrections for a given word. The spelling.correct() command returns the corrected version (best guess) of the word.
"""

print( en.spelling.suggest("comptuer") )
# >>> ['computer']

    

"""
Shallow parsing, the grammatical structure of a sentence

NodeBox English Linguistics is able to do sentence structure analysis using a combination of Jason Wiener's tagger and NLTK's chunker. The tagger assigns a part-of-speech tag to each word in the sentence using a (Brill's) lexicon. A postag is something like NN or VBP marking words as nouns, verbs, determiners, pronouns, etc. The chunker is then able to group syntactic units in the sentence. A syntactic unit is, for example, a determiner followed by adjectives followed by a noun: the tasty little chicken is a syntactic unit.

The sentence.tag() command tags the given sentence. The return value is a list of (word, tag) tuples. However, when you print it out it will look like a string.
"""

print( en.sentence.tag("this is so cool") )
# >>> this/DT is/VBZ so/RB cool/JJ

"""
There are lots of part-of-speech tags and it takes some time getting to know them. The full list is here. The sentence.tag_description() returns a (description, examples) tuple for a given tag:
"""

print( en.sentence.tag_description("NN") )
# >>> ('noun, singular or mass', 'tiger, chair, laughter')

"""
The sentence.chunk() command returns the chunked sentence:
"""

pp( en.sentence.chunk("we are going to school") )
# >>> [['SP',
# >>>   ['NP', ('we', 'PRP')],
# >>>   ['AP',
# >>>   ['VP', ('are', 'VBP'), ('going', 'VBG'), ('to', 'TO')],
# >>>   ['NP', ('school', 'NN')]]]]

"""
Now what does all this mean?

    NP: noun phrases, syntactic units describing a noun, for example: a big fish.
    VP: verb phrases, units of verbs and auxillaries, for example: are going to.
    AP: a verb/argument structure, a verb phrase and a noun phrase being influenced.
    SP: a subject structure: a noun phrase which is the executor of a verb phrase or verb/argument structure.

A handy sentence.traverse(sentence, cmd) command lets you feed a chunked sentence to your own command chunk by chunk:
"""

s = "we are going to school"
def callback(chunk, token, tag):
    if chunk != None : 
        print( en.sentence.tag_description(chunk)[0].upper() )
    if chunk == None : 
        print( token, "("+en.sentence.tag_description(tag)[0]+")" )
en.sentence.traverse(s, callback)
# >>> SUBJECT PHRASE
# >>> NOUN PHRASE
# >>> we (pronoun, personal)
# >>> VERB PHRASE AND ARGUMENTS
# >>> VERB PHRASE
# >>> are (verb, non-3rd person singular present)
# >>> going (verb, gerund or present participle)
# >>> to (infinitival to)
# >>> NOUN PHRASE
# >>> school (noun, singular or mass)

"""
A even handier sentence.find(sentence, pattern) command lets you find patterns of text in a sentence:
"""

s = "The world is full of strange and mysterious things."
print( en.sentence.find(s, "JJ and JJ NN") )
# >>> [[('strange', 'JJ'), ('and', 'CC'), 
# >>>   ('mysterious', 'JJ'), ('things', 'NNS')]]

"""
The returned list contains all chunks of text that matched the pattern. In the example above it retrieved all chunks of the form an adjective + and + an adjective + a noun. Notice that when you use something like "NN" in your pattern (noun), NNS (plural nouns) are returned as well.
"""

s = "The hairy hamsters visited the cruel dentist."
matches = en.sentence.find(s, "JJ NN")
print( matches )
# >>> [[('hairy', 'JJ'), ('hamsters', 'NNS')], [('cruel', 'JJ'), ('dentist', 'NN')]]

"""
An optional chunked parameter can be set to False to return strings instead of token/tag tuples. You can put pieces of the pattern between brackets to make them optional, or use wildcards:
"""

s = "This makes the parser an extremely powerful tool."
print( en.sentence.find(s, "(extreme*) (JJ) NN", chunked=False) )
# >>> ['parser', 'extremely powerful tool']

"""
Finally, if you feel up to it you could feed the following command with a list of your own regular expression units to chunk, mine are pretty basic as I'm not a linguist.
"""

print( en.sentence.chunk_rules() )

 

"""
Summarisation of text to keywords

NodeBox English Linguistics is able to strip keywords from a given text.


en.content.keywords(txt, top=10, nouns=True, singularize=True, filters=[])


The content.keywords() command guesses a list of words that frequently occur in the given text. The return value is a list (length defined by top) of (count, word) tuples. When nouns is True, returns only nouns. The command furthermore ignores connectives, numbers and tags. When singularize is True, attempts to singularize nouns in the text. The optional filters parameter is a list of words which the command should ignore.

So, assuming you would want to summarise web content you can do the following:
"""

from urllib import urlopen
html = urlopen("http://news.bbc.co.uk/").read()
meta = ["news", "health", "uk", "version", "weather", 
        "video", "sport", "return", "read", "help"]

print( en.commonsense.sentence_keywords(html, filters=meta) )
# >>> [(6, 'funeral'), (5, 'beirut'), (3, 'war'), (3, 'service'), (3, 'radio'), 
# >>>  (3, 'lebanon'), (3, 'islamist'), (3, 'function'), (3, 'female')]

 
"""
Regressive Imagery Dictionary, psychological content analysis

NodeBox English Linguistics is able to do psychological content analysis using John Wiseman's Python implementation of the Regressive Imagery Dictionary. The RID asigns scores to primary, secondary and emotional process thoughts in a text.

    Primary: free-form associative thinking involved in dreams and fantasy
    Secondary: logical, reality-based and focused on problem solving
    Emotions: expressions of fear, sadness, hate, affection, etc. 


en.content.categorise(str)


The content.categorise() command returns a sorted list of categories found in the text. Each item in the list has the following properties:

    item.name: the name of the category
    item.count: the number of words in the text that fall into this category
    item.words: a list of words from the text that fall into this category
    item.type: the type of category, either "primary", "secondary" or "emotions".

Let's run a little test with Lucas' Ideas from the Heart text:
"""

txt = open("heart.txt").read()
summary = en.content.categorise(txt)
print( summary.primary )
print( summary.secondary )
print( summary.emotions )
# >>> 0.290155440415
# >>> 0.637305699482
# >>> 0.0725388601036
# Lucas' text has a 64% secondary value.

# The top 5 categories in the text:
for category in summary[:5]:
    print( category.name, category.count )
# >>> instrumental behavior 30
# >>> abstraction 30
# >>> social behavior 28
# >>> temporal references 24
# >>> concreteness 18

# Words in the top "instrumental behavior" category:
print( summary[0].words )
# >>> ['students', 'make', 'students', 'reached', 'countless', 
# >>>  'student', 'workshop', 'workshop', 'students', 'finish', 
# >>>  'spent', 'produce', 'using', 'work', 'students', 'successful', 
# >>>  'workshop', 'students', 'pursue', 'skills', 'use', 
# >>>  'craftsmanship', 'use', 'using', 'workshops', 'workshops', 
# >>>  'result', 'students', 'workshops', 'student']

"""
You can find all the categories for primary, secondary and emotional scores in the en.rid.primary, en.rid.secondary and en.rid.emotions lists.

 

 

 
Ogden's basic English words

NodeBox English Linguistics comes bundled with Charles K. Ogden list of basic English words: a set of 2000 words that can express 90% of the concepts in English. The list is stored as en.basic.words. It can be filtered for nouns, verbs, adjectives and adverbs:
"""

print( en.basic.words )
# >>> ['a', 'able', 'about', 'account', 'acid', 'across', ... ]

print( en.basic.verbs )
# >>> ['account', 'act', 'air', 'amount', 'angle', 'answer', ... ]
