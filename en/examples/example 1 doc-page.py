"""
How to get the library up and running

Put the en library folder in the same folder as your script so NodeBox can find the library. You can also put it in ~/Library/Application Support/NodeBox/. It takes some time to load all the data the first time.
"""

from __future__ import print_function

import pprint
pp = pprint.pprint

en = ximport("en")

 

"""
Categorise words as nouns, verbs, numbers and more

The is_number() command returns True when the given value is a number:
"""

print()
print( "12 is a number:", )
print( en.is_number(12) )

print()
print( "'twelve' is a number:", )
print( en.is_number("twelve") )

"""
The is_noun() command returns True when the given string is a noun. You can also check for is_verb(), is_adjective() and is_adverb():
"""

print()
print( "'banana' is a noun:", )
print( en.is_noun("banana") )


"""
The is_tag() command returns True when the given string is a tag, for example HTML or XML.

The is_html_tag() command returns True when the string is a HTML tag.
"""

print()
print( "'div' is a html-tag:", )
print( en.is_html_tag('<div/>') )

"""
Categorise words as emotional, persuasive or connective

The is_basic_emotion() command returns True if the given word expresses a basic emotion (anger, disgust, fear, joy, sadness, surprise):
"""

print()
print( "'cheerful' is a basic emotion?:",  )
print( en.is_basic_emotion("cheerful") )

"""
The is_persuasive() command returns True if the given word is a "magic" word (you, money, save, new, results, health, easy, ...):

"""

print()
print( "'money' is persuasive?:",  )
print( en.is_persuasive("money") )

"""
The is_connective() command returns True if the word is a connective (nevertheless, whatever, secondly, ... and words like I, the, own, him which have little semantical value):
"""

print()
print( "'but' is a connective?:",  )
print( en.is_connective("but") )


"""
Converting between numbers and words

The number.ordinal() command returns the ordinal of the given number, 100 yields 100th, 3 yields 3rd and twenty-one yields twenty-first:
"""

print()
print( "'100' ordinal:",  )
print( en.number.ordinal(100) )

print()
print( "'twenty-one' ordinal:",  )
print( en.number.ordinal("twenty-one") )


"""
The number.spoken() command writes out the given number:
"""

print()
print( "'25' spoken:",  )
print( en.number.spoken(25) )


"""
Quantification of numbers and lists

The number.quantify() command quantifies the given word:
"""

print()
print( "quantify 10 chicken:", )
print( en.number.quantify(10, "chicken") )

print()
print( "quantify 100 chicken:", )
print( en.number.quantify(800, "chicken") )
# >>> a number of chickens
# >>> hundreds of chickens

"""
The list.conjunction() command quantifies a list of words. Notice how goose is correctly pluralized and duck has the right article.

"""
farm = ["goose", "goose", "chicken", "chicken", "chicken"]
print()
print( 'conjunction ["goose", "goose", "chicken", "chicken", "chicken"]:', )
print( en.list.conjunction(farm) )


"""
You can also quantify the types of things in the given list, class or module:
"""

print()
print( 'conjunction [1,2,3,4,5]:', )
print( en.list.conjunction((1,2,3,4,5), generalize=True) )

print()
print( 'conjunction "en":', )
print( en.list.conjunction(en, generalize=True) )
# >>> several integers
# >>> a number of modules, a number of functions, a number of strings, 
# >>> a pair of lists, a pair of dictionaries, an en verb, an en sentence, 
# >>> an en number, an en noun, an en list, an en content, an en adverb, 
# >>> an en adjective, a None type and a nodebox graphics cocoa Context class

 

"""
Indefinite article: a or an

The noun.article() returns the noun with its indefinite article:
"""

print()
print( "Noun article 'university':", )
print( en.noun.article("university") )

print( "Noun article 'owl':", )
print( en.noun.article("owl") )

print( "Noun article 'hour':", )
print( en.noun.article("hour") )
# >>> a university
# >>> an owl
# >>> an hour

 

"""
Pluralization and singularization of nouns

The noun.plural() command pluralizes the given noun:
"""

print( "Plural 'child':", )
print( en.noun.plural("child") )

print( "Plural 'kitchen knife':", )
print( en.noun.plural("kitchen knife") )

print( "Plural 'wolf':", )
print( en.noun.plural("wolf") )

print( "Plural 'part-of-speech':", )
print( en.noun.plural("part-of-speech") )
# >>> children
# >>> kitchen knives
# >>> wolves
# >>> parts-of-speech

"""
You can also do adjective.plural().

An optional classical parameter is True by default and determines if either classical or modern inflection is used (e.g. classical pluralization of octopus yields octopodes instead of octopuses).

The noun.singular() command singularizes the given plural:
"""

print()
print( "Singular 'people':", )
print( en.noun.singular("people") )
# >>> person

 

"""
Emotional value of a word

The noun.is_emotion() guesses whether the given noun expresses an emotion by checking if there are synonyms of the word that are basic emotions. Returns True or False by default.
"""

print()
print( "Noun is emotion 'anger':", )
print( en.noun.is_emotion("anger") )
# >>> True

"""
Or you can return a string which provides some information with the boolean=False parameter.
"""

print()
print( "Adjective is emotion 'anxious':", )
print( en.adjective.is_emotion("anxious", boolean=False) )
# >>> fear

"""
An additional optional parameter shallow=True speeds up the lookup process but doesn't check as many synonyms. You can also use verb.is_emotion(), adjective.is_emotion() and adverb.is_emotion().

 

WordNet glossary, synonyms, antonyms, components

WordNet describes semantic relations between synonym sets.

The noun.gloss() command returns the dictionary description of a word:
"""

print()
print( "Glossary 'book':", )
print( en.noun.gloss("book") )
# >>> a written work or composition that has been published (printed on pages 
# >>> bound together); "I am reading a good book on economics"

"""
A word can have multiple senses, for example "tree" can mean a tree in a forest but also a tree diagram, or a person named Sir Herbert Beerbohm Tree:
"""

print()
print( "Senses 'tree':", )
print( en.noun.senses("tree") )
# >>> [['tree'], ['tree', 'tree diagram'], ['Tree', 'Sir Beerbohm Tree']]

print( "Senses 'tree' sense=1:", )
print( en.noun.gloss("tree", sense=1) )
# >>> a figure that branches from a single root; "genealogical tree"

"""
The noun.lexname() command returns a categorization for the given word:
"""

print()
print( "Lexname 'book':", )
print( en.noun.lexname("book") )
# >>> communication

"""
The noun.hyponym() command return examples of the given word:
"""

print()
print( "Hyponym 'vehicle':", )
print( en.noun.hyponym("vehicle") )
# >>> [['bumper car', 'Dodgem'], ['craft'], ['military vehicle'], ['rocket', 
# >>>  'projectile'], ['skibob'], ['sled', 'sledge', 'sleigh'], ['steamroller', 
# >>>  'road roller'], ['wheeled vehicle']]

print()
print( "Hyponym 'tree' sense=1:", )
print( en.noun.hyponym("tree", sense=1) )
# >>> [['cladogram'], ['stemma']]

"""
The noun.hypernym() command return abstractions of the given word:
"""

print()
print( "Hypernym 'earth':", )
print( en.noun.hypernym("earth") )
print( "Hypernym 'earth' sense=1:", )
print( en.noun.hypernym("earth", sense=1) )
# >>> [['terrestrial planet']]
# >>> [['material', 'stuff']]

"""
You can also execute a deep query on hypernyms and hyponyms. Notice how returned values become more and more abstract:
"""

print()
print( "Hypernyms 'vehicle' sense=0:" )
pp( en.noun.hypernyms("vehicle", sense=0) )
# >>> [['vehicle'], ['conveyance', 'transport'], 
# >>>  ['instrumentality', 'instrumentation'], 
# >>>  ['artifact', 'artefact'], ['whole', 'unit'], 
# >>>  ['object', 'physical object'], 
# >>>  ['physical entity'], ['entity']]

"""
The noun.holonym() command returns components of the given word:
"""

print()
print( "Holonym 'computer':" )
pp( en.noun.holonym("computer") )
# >>> [['busbar', 'bus'], ['cathode-ray tube', 'CRT'], 
# >>>  ['central processing unit', 'CPU', 'C.P.U.', 'central processor', 
# >>>   'processor', 'mainframe'] ...

"""
The noun.meronym() command returns the collection in which the given word can be found:
"""

print()
print( "Meronym 'tree':" )
print( en.noun.meronym("tree") )
# >>> [['forest', 'wood', 'woods']]

"""
The noun.antonym() returns the semantic opposite of the word:
"""

print()
print( "Antonym 'black':" )
print( en.noun.antonym("black") )
# >>> [['white', 'whiteness']]

"""
Find out what two words have in common:
"""

print()
print( "Meet 'cat', 'dog':  sense1=0, sense2=0" )
print( en.noun.meet("cat", "dog", sense1=0, sense2=0) )
print( "Meet 'cat', 'dog':  sense1=1, sense2=1" )
print( en.noun.meet("cat", "dog", sense1=1, sense2=1) )
# >>> [['carnivore']]

"""
The noun.absurd_gloss() returns an absurd description for the word:
"""

print()
print( "Absurd glossary 'typography':" )
print( en.noun.absurd_gloss("typography") )
# >>> a business deal on a trivial scale

"""
The return value of a WordNet command is usually a list containing other lists of related words. You can use the en.list.flatten() command to flatten the list:
"""

print()
print( "Flattened senses 'tree':" )
print( en.list.flatten(en.noun.senses("tree")) )
# >>> ['tree', 'tree', 'tree diagram', 'Tree', 'Sir Herbert Beerbohm Tree']

"""
If you want a list of all nouns/verbs/adjectives/adverbs there's the wordnet.all_nouns(), wordnet.all_verbs() ... commands:
"""

print()
print( "Count of wordnet nouns:",  )
print( len(en.wordnet.all_nouns()) )
# >>> 117096

"""
All of the commands shown here for nouns are also available for verbs, adjectives and adverbs, en.verb.hypernyms("run"), en.adjective.gloss("beautiful") etc. are valid commands.
"""

 
