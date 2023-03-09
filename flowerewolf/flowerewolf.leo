<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20230227153025.2" a="E"><vh>code</vh>
<v t="karstenw.20230227153059.1" a="E"><vh>@clean __init__.py</vh>
<v t="karstenw.20230227153123.1"><vh>Declarations</vh></v>
<v t="karstenw.20230227161027.1"><vh>Globals</vh></v>
<v t="karstenw.20230227153522.1" a="E"><vh>+ GRAMMAR +</vh>
<v t="karstenw.20230227153123.2"><vh>alliterations</vh></v>
<v t="karstenw.20230227153123.3"><vh>nouns</vh></v>
<v t="karstenw.20230227153123.4"><vh>adjectives</vh></v>
<v t="karstenw.20230227153123.5"><vh>verbs</vh></v>
<v t="karstenw.20230227153123.6"><vh>alliterate</vh></v>
<v t="karstenw.20230227153123.7"><vh>eloquate</vh></v>
<v t="karstenw.20230227153123.8"><vh>consonate</vh></v>
<v t="karstenw.20230227153123.9"><vh>incorporate</vh></v>
<v t="karstenw.20230227153123.10"><vh>verse</vh></v>
</v>
<v t="karstenw.20230227153123.11" a="E"><vh>dada</vh>
<v t="karstenw.20230227162021.1"><vh>&lt;&lt; Setup the colors and fonts &gt;&gt;</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230227153025.2"></t>
<t tx="karstenw.20230227153059.1">@language python
@tabwidth -4
@others

</t>
<t tx="karstenw.20230227153123.1"># FLOWEREWOLF - last updated for NodeBox 1.9.2
# Author: Tom De Smedt &lt;tomdesmedt@organisms.be&gt;
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


</t>
<t tx="karstenw.20230227153123.10">def verse(word):
    
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
        if random() &gt; 0.6:
            
            if w in allnouns:
                w = incorporate(w).upper()
            if w in allverbs:
                w = incorporate(w, VERB)
            if w in alladjectives:
                w = incorporate(w, ADJECTIVE)
            
        if i &gt; 0 and i % 3 == 0:
            words[i] = words[i] + "\n"
            
        words[i] = w
            
    g = " ".join(words)
    g = g.replace("type A ", "!")
    g = g.replace("group A ", "!")
    return g


</t>
<t tx="karstenw.20230227153123.11">def dada(query, foreground=None, background=None, fonts=[], transparent=False):

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

    &lt;&lt; Setup the colors and fonts &gt;&gt;

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
                if random() &gt; 0.7: 
                    _ctx.fontsize(random(f*0.6, f*1.2))
                
                # A word that is s
                #                 l
                #                  a
                #                   n
                #                    t
                #                     e
                #                      d.
                #                       The text continues on the next line.
                if random() &gt; 0.9:
                    _ctx.rotate(-45 * random(1, 2))
                    _ctx.text(word+" ", x, y+_ctx.textwidth(word)/2)
                    y += _ctx.textwidth(word) * 1.5
                    _ctx.reset()
                
                # ...or we continue on this line as normal:
                else:

                    # The word is sometimes printed DESREVNI:
                    # e.g red text in white box instead of white text on red.
                    # Some wiggling occurs.
                    if random() &gt; 0.85:    
                        r = random(50)
                        if random() &gt; 0.8: _ctx.oval(x, y, r, r)
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
                    if random() &gt; 0.99:
                        _ctx.text(word+" ", x, y+_ctx.textheight(word))
                    
                    # Add a line for visual effect,.
                    if random() &gt; 0.9:
                        d = random(100)
                        _ctx.stroke(foreground)
                        _ctx.strokewidth(0.5)
                        _ctx.line(x + _ctx.textwidth(word),     y,
                                  x + _ctx.textwidth(word) + d, y)
                        x += d
                    
                    # Some play with indentation.
                    # Now where did I leave that oval?
                    x += _ctx.textwidth(word+" ")
                    if x &gt; _ctx.WIDTH * 0.65:
                        x = _ctx.WIDTH / 15
                        y += _ctx.textheight(word)
            
            x = _ctx.WIDTH / 15
            y += _ctx.textheight(word)
</t>
<t tx="karstenw.20230227153123.2">def alliterations(head="", tail=""):

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


</t>
<t tx="karstenw.20230227153123.3">def nouns(list):
    
    """Parses nouns from a list of words.
    """
    
    words = []
    for word in list:
        word = word.strip()
        if word in allnouns:
            words.append(word)
    return words


</t>
<t tx="karstenw.20230227153123.4">def adjectives(list):
    
    """Parses adjectives from a list of words.
    """
    
    words = []
    for word in list:
        word = word.strip()
        if word in alladjectives:
            words.append(word)
    return words


</t>
<t tx="karstenw.20230227153123.5">def verbs(list):
    
    """Parses verbs from a list of words.
    """
    
    words = []
    for word in list:
        word = word.strip()
        if word in allverbs:
            words.append(word)
    return words


</t>
<t tx="karstenw.20230227153123.6">def alliterate(word, typ=ADJECTIVE):
    
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

</t>
<t tx="karstenw.20230227153123.7">def eloquate(noun, antonise=True):
    
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
                     and len( str(antonym)) &gt; 0 )
                and random() &gt; 0.4 ):
            antonym = choice(choice(antonym))
            return "no " + eloquate(antonym, antonise=False)
    else:
        if antonise:
            if antonym:
                if random() &gt; 0.4:
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
    elif random() &gt; 0.2:
        return adjective + " " + noun
    elif random() &gt; 0.5:
        return noun + " " + adjective
    else:
        return noun + " so " + adjective


</t>
<t tx="karstenw.20230227153123.8">def consonate(verb, noun):
    
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
    if len(verbs) &gt; 0: return choice(verbs)
    
    return verb
    
</t>
<t tx="karstenw.20230227153123.9">def incorporate(word, typ=NOUN):
    
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
        if len(a) &gt; 0:
            tail = choice(a)
            if random() &gt; 0.25: 
                if i &gt; len(word):
                    return tail
                return word + tail[i:]
        
    return word + tail[i:]


</t>
<t tx="karstenw.20230227153522.1"></t>
<t tx="karstenw.20230227161027.1">NOUN = "noun"
ADJECTIVE = "adjective"
VERB = "verb"

old = False

</t>
<t tx="karstenw.20230227162021.1"># Setup the colors and fonts.

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

</t>
</tnodes>
</leo_file>
