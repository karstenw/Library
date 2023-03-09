# FLOWEREWOLF - last updated for NodeBox 1.9.2
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# Copyright (c) 2004-2007 by Tom De Smedt.
# Licensed under GPL, see LICENSE.txt for details.

################################################################################

import pdb

import time
import io
import pprint
pp = pprint.pprint

from nodebox.util import random, choice

# old en lib
if 0:
    import en
    import en.wordnet
    wordnet = en.wordnet

# new linguistics/pattern
if 1:
    # need to import linguistics first - sets up sys.path and corpus/data folders for the sublibs
    import linguistics
    import pattern
    import pattern.text
    import pattern.text.en
    en = pattern.text.en
    wordnet = en.wordnet


allnouns = set( wordnet.NOUNS() )
allverbs = set( wordnet.VERBS() )
alladjectives = set( wordnet.ADJECTIVES() )

f = io.open("vocabulary.txt", 'r', encoding="utf-8")
dictionary = f.readlines()
f.close()


NOUN = "noun"
ADJECTIVE = "adjective"
VERB = "verb"

old = False

def alliterations(head="", tail=""):

    """Returns alliterations for the given criteria.
    
    The list of words returned have the given starting characters,
    and the given ending characters.
    
    """
    words = []
    for word in dictionary:
        if (    (head=="" or word[:len(head)]== head)
            and (tail=="" or word.strip()[-len(tail):]== tail)):
            words.append(word)
    return words


def nouns(list):
    
    """Parses nouns from a list of words.
    """
    
    words = []
    for word in list:
        word = word.strip()
        if word in allnouns:
            words.append(word)
    return words


def adjectives(list):
    
    """Parses adjectives from a list of words.
    """
    
    words = []
    for word in list:
        word = word.strip()
        if word in alladjectives:
            words.append(word)
    return words


def verbs(list):
    
    """Parses verbs from a list of words.
    """
    
    words = []
    for word in list:
        word = word.strip()
        if word in allverbs:
            words.append(word)
    return words


def alliterate(word, typ=ADJECTIVE):
    
    """Returns an alliteration of the given word.
    
    When a noun is supplied, returns an adjective alliteration.
    When an adjective is supplied, returns a noun alliteration.
    When a verb is supplied, returns a infinitive verb alliteration.
    Attempts to alliterate as strongly as possible,
    with the three starting characters and two ending characters,
    and gradually weakens down when no results are found.
    
    """
    
    if typ == NOUN:        f = adjectives
    if typ == ADJECTIVE:   f = nouns
    if typ == VERB:
        if old:
            word = en.verb.infinitive(word)
        else:
            pdb.set_trace()
            word = en.verbs.conjugate(word, en.INFINITIVE)
        f = verbs
    
    x = alliterations(word[0:3], word[-2:])
    x = f(x)

    if len(x) == 0 or x[0] == word:
        x = alliterations(word[0:3], word[-1:])
        x = f(x)
    
    if len(x) == 0 or x[0] == word:
        x = alliterations(word[0], word[-1:])
        x = f(x)
        
    if len(x) == 0 or x[0] == word:
        x = alliterations(word[0])
        x = f(x)
    
    try: 
        alliteration = choice(x)
        return alliteration
    except:
        return None

def eloquate(noun, antonise=True):
    
    """Returns an alliteration with an adjective.
    
    Picks a synonym for the given noun from WordNet.
    Alliterates an adjective for this synonym.
    
    """

    if type(noun) in (str,):
        synsets = wordnet.synsets( noun )
        if synsets:
            synset = synsets[0]
            hyponyms = list( synset.hyponyms() )
            noun = synset

    if old:
        antonym = en.noun.antonym(noun)
    else:
        antonym = noun.antonym

    if old:
        if (        antonise
                and (    antonym
                     and len( str(antonym)) > 0 )
                and random() > 0.4 ):
            antonym = choice(choice(antonym))
            return "no " + eloquate(antonym, antonise=False)
    else:
        if antonise:
            if antonym:
                if random() > 0.4:
                    return "no " + eloquate(antonym, antonise=False)

    if old:    
        noun = choice(choice(en.noun.hyponyms(noun)))
    else:
        hyponyms = []
        for h in wordnet.synsets( noun ):
            hyponyms.extend( list(h.hyponyms()) )
        if hyponyms:
            noun = choice( hyponyms )
    
    adjective = alliterate(noun, typ=NOUN)
    if adjective == None:
        if old:
            noun = choice(choice(en.noun.hypernyms(noun)))
            adjective = alliterate(noun, typ=NOUN)
        else:
            hypernyms = []
            for h in wordnet.synsets( noun ):
                hypernyms.extend( list(h.hypernyms()) )
            if hypernyms:
                noun = choice( hyponyms )
                adjective = alliterate(noun, typ=NOUN)
        
    if adjective == None:
        return noun
    elif random() > 0.2:
        return adjective + " " + noun
    elif random() > 0.5:
        return noun + " " + adjective
    else:
        return noun + " so " + adjective


def consonate(verb, noun):
    
    """Match a consonating verb synonym to the noun.
    
    Finds a synonym of the given noun,
    that has the same ending characters.
    
    """
    
    try:
        h = en.verb.hyponym(verb)
        h = en.wordnet.flatten(h)
    except:
        return verb
    
    verbs = []
    for v in h:
        if v[-1:] == noun[-1:]: verbs.append(v)
    if len(verbs) > 0: return choice(verbs)
    
    return verb
    
def incorporate(word, typ=NOUN):
    
    """Combines this noun with another.
    
    This results in invented words that have a double meaning, 
    for instance the lyrical "flowerewolf" that is even a palindrome!
    
    By specifying a type (None, NOUN, ADJECTIVE, ADVERB),
    you can specify what kind of word to mix in.
    
    """
    
    if typ == NOUN:
        f = nouns
    if typ == ADJECTIVE:
        f = adjectives
    if typ == VERB:
        word = en.verb.infinitive(word)
        f = verbs
    
    for i in [4,3,2,1]:
        a = alliterations(head=word[-i:])
        if typ != None:
            a = f(a)
        if len(a) > 0:
            tail = choice(a)
            if random() > 0.25: 
                if i > len(word):
                    return tail
                return word + tail[i:]
        
    return word + tail[i:]


def verse(word):
    
    """Creates a small rhyme for a given word.
    
    The rhyme is based on WordNet's description for the word.
    This description is eloquated (alliterated or antonated), incorporated.
    
    """

    if old:
        g = en.noun.gloss(word)
    else:
        g = word.gloss

    words = g.split(" ")

    pdb.set_trace()
    for i in range(len(words)):
        
        w = words[i]
        w = w.replace("\"", "")
        
        if w in allnouns:
            w = eloquate(w)
            if type(w) not in (str,):
                w = w.senses[0]
            # w = w.lemma
        if random() > 0.6:
            
            if w in allnouns:
                w = incorporate(w).upper()
            if w in allverbs:
                w = incorporate(w, VERB)
            if w in alladjectives:
                w = incorporate(w, ADJECTIVE)
            
        if i > 0 and i % 3 == 0:
            words[i] = words[i] + "\n"
            
        words[i] = w
            
    g = " ".join(words)
    g = g.replace("type A ", "!")
    g = g.replace("group A ", "!")
    return g


def dada(query, foreground=None, background=None, fonts=[], transparent=False):

    """Create some lines of poetry based on the query."""

    print("query:", query)

    # en
    if old:
        h = en.noun.hyponyms(query)
        h = choice(en.wordnet.flatten(h))

    # alternate hyponyms with pattern.wordnet
    else:
        # pdb.set_trace()
        synsets = wordnet.synsets( query )
        h = []
        for synset in synsets:
            hyponyms = synset.hyponyms()
            for hyponym in hyponyms:
                if 0:
                    lemmas = hyponym.lemmas()
                    for lemma in lemmas:
                        h.append( lemma )
                if 1:
                    h.append( hyponym )
        # h = list( h )

    print("hyponyms for '%s':  %s" % (query, str(h)) )
    w = choice( h )

    lines = verse(w)
    lines = lines.split("\n")

    # Setup the colors and fonts.

    if foreground == None: 
        foreground = _ctx.color(1,1,1)

    if background == None:
        background = _ctx.color(1,0,0)

    if len(fonts) == 0: 
        fonts = [_ctx.font()]

    f = _ctx.fontsize()
    _ctx.background(background)

    if transparent: 
        _ctx.background(None)

    _ctx.lineheight(1)
    _ctx.fill(foreground)
    _ctx.stroke(foreground)
    _ctx.strokewidth(0.5)


    # Poem title.
    _ctx.text(query, _ctx.WIDTH / 15, _ctx.HEIGHT / 7-f)
    
    for i in range(1):
        
        _ctx.fill(foreground)
        x = _ctx.WIDTH / 15
        y = _ctx.HEIGHT / 7
        
        for words in lines:
            for word in words.split(" "):
                
                # For each word in a line,
                # pick a random font from the list and a random fontsize.
                _ctx.font(choice(fonts))
                if random() > 0.7: 
                    _ctx.fontsize(random(f*0.6, f*1.2))
                
                # A word that is s
                #                 l
                #                  a
                #                   n
                #                    t
                #                     e
                #                      d.
                #                       The text continues on the next line.
                if random() > 0.9:
                    _ctx.rotate(-45 * random(1, 2))
                    _ctx.text(word+" ", x, y+_ctx.textwidth(word)/2)
                    y += _ctx.textwidth(word) * 1.5
                    _ctx.reset()
                
                # ...or we continue on this line as normal:
                else:

                    # The word is sometimes printed DESREVNI:
                    # e.g red text in white box instead of white text on red.
                    # Some wiggling occurs.
                    if random() > 0.85:    
                        r = random(50)
                        if random() > 0.8: _ctx.oval(x, y, r, r)
                        _ctx.rotate(random(-3, 3))
                        _ctx.nostroke()
                        _ctx.rect(
                            x-2, 
                            y-_ctx.textheight(word), 
                            _ctx.textwidth(word)+4,
                            _ctx.textheight(word)
                        )
                        _ctx.fill(background)
                        _ctx.text(word+" ", x, y)
                        _ctx.fill(foreground)
                    
                    # Otherwise, just print out the word.
                    else:
                        _ctx.text(word+" ", x, y)
                    
                    # Word is repeated for poetic stress effect.
                    #         repeated
                    if random() > 0.99:
                        _ctx.text(word+" ", x, y+_ctx.textheight(word))
                    
                    # Add a line for visual effect,.
                    if random() > 0.9:
                        d = random(100)
                        _ctx.stroke(foreground)
                        _ctx.strokewidth(0.5)
                        _ctx.line(x + _ctx.textwidth(word),     y,
                                  x + _ctx.textwidth(word) + d, y)
                        x += d
                    
                    # Some play with indentation.
                    # Now where did I leave that oval?
                    x += _ctx.textwidth(word+" ")
                    if x > _ctx.WIDTH * 0.65:
                        x = _ctx.WIDTH / 15
                        y += _ctx.textheight(word)
            
            x = _ctx.WIDTH / 15
            y += _ctx.textheight(word)

