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
<v t="karstenw.20230310124746.1"><vh>FlowerWord</vh>
<v t="karstenw.20230310124806.1"><vh>__init__</vh></v>
<v t="karstenw.20230310125018.1"><vh>hyponyms</vh></v>
<v t="karstenw.20230319115908.1"><vh>hypernyms</vh></v>
</v>
<v t="karstenw.20230310134343.1"><vh>printsynset</vh></v>
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
<v t="karstenw.20230227153123.11" a="E"><vh>dada</vh>
<v t="karstenw.20230227162021.1"><vh>&lt;&lt; Setup the colors and fonts &gt;&gt;</vh></v>
</v>
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

import time
import io

kwdbg = 1
import pdb
import pprint
pp = pprint.pprint

from random import seed
from nodebox.util import random, choice

# seed(1)

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


</t>
<t tx="karstenw.20230227153123.10">def verse(word):
    
    """Creates a small rhyme for a given word.
    
    The rhyme is based on WordNet's description for the word.
    This description is eloquated (alliterated or antonated), incorporated.
    
    """
    fword = FlowerWord( word )
    if old:
        g = en.noun.gloss(word)
    elif False:
        g = wordnet.synsets( word )[0].gloss #word.gloss

    g = fword.gloss
    words = g.split(" ")

    # pdb.set_trace()

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
    if kwdbg:
        pp( ("verse():", word, g) )
    return g


</t>
<t tx="karstenw.20230227153123.11">def dada(query, foreground=None, background=None, fonts=[], transparent=False):

    """Create some lines of poetry based on the query."""

    print("dada() query:", query)

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
                # pdb.set_trace()
                if 1:
                    synonyms = hyponym.synonyms
                    for synonym in synonyms:
                        if '_' in synonym:
                            synonym = synonym.replace("_", " ")
                        h.append( synonym )
                if 0:
                    h.append( hyponym )
        # h = list( h )

    if kwdbg:
        print("dada() hyponyms for '%s':" % (query,), h )
    if h:
        w = choice( h )
    else:
        w = "Dummy"

    lines = verse(w)
    lines = lines.split("\n")

    &lt;&lt; Setup the colors and fonts &gt;&gt;

    # Poem title.
    _ctx.text(query, _ctx.WIDTH / 15, _ctx.HEIGHT / 7-f)
    
    # initially spanned the rest of dada()
    # for i in range(1):
        
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

    if type(head) not in (str,):
        pdb.set_trace()
        print(head,tail)
    if type(tail) not in (str,):
        pdb.set_trace()
        print(head,tail)

    h = head.lower()
    t = tail.lower()

    for word in dictionary:
        if (    (   h == ""
                 or word.startswith(h))
            and (   t == ""
                 or word.endswith(t))):
            words.append(word)
    if 0: # kwdbg:
        print("alliterations(): '%s'  '%s' -&gt; %s" % (head, tail, str(words) ) )
    return words


</t>
<t tx="karstenw.20230227153123.3">def nouns( words ):
    
    """Parses nouns from a list of words.
    """
    
    result = []
    for word in words:
        word = word.strip()
        if word in allnouns:
            result.append(word)
    return result


</t>
<t tx="karstenw.20230227153123.4">def adjectives( words ):
    
    """Parses adjectives from a list of words.
    """
    
    result = []
    for word in words:
        word = word.strip()
        if word in alladjectives:
            result.append(word)
    return result


</t>
<t tx="karstenw.20230227153123.5">def verbs( words ):
    
    """Parses verbs from a list of words.
    """
    
    result = []
    for word in words:
        word = word.strip()
        if word in allverbs:
            result.append(word)
    return result


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
        if kwdbg:
            print("alliterate():", word, typ, alliteration, x)
        return alliteration
    except:
        return None

</t>
<t tx="karstenw.20230227153123.7">def eloquate(noun, antonise=True):
    
    """Returns an alliteration with an adjective.
    
    Picks a synonym for the given noun from WordNet.
    Alliterates an adjective for this synonym.
    
    """
    
    fword = FlowerWord( noun )
    antonym = fword.antonym

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
                if 1: #random() &gt; 0.4:
                    # antonym = choice(choice(antonym))
                    try:
                        result = "no " + eloquate(antonym, antonise=False)
                    except TypeError as err:
                        pdb.set_trace()
                        print(err)
                        print(result)

                    print("eloquate '%s' eloquate(antonym='%s') result:" % (noun,antonym), result )
                    return result

    if old:    
        noun = choice(choice(en.noun.hyponyms(noun)))
    else:
        hyponyms = []
        hyponyms = fword.hyponyms()
        if hyponyms:
            pp( ("eloquate hyponyms:", noun, hyponyms) )
            hyponym = choice( hyponyms )
            hyponym = hyponym.replace("_", " ")
            if kwdbg:
                print("eloquate() Hyponym for noun %s:" % (repr(noun),), hyponym)
            noun = hyponym
    # pdb.set_trace()

    adjective = alliterate(noun, typ=NOUN)
    if adjective == None:
        if old:
            noun = choice(choice(en.noun.hypernyms(noun)))
            adjective = alliterate(noun, typ=NOUN)
        else:
            hypernyms = fword.hypernyms()
            pp( ("eloquate hypernyms:", noun, hypernyms) )

            if hypernyms:
                noun = choice( hyponyms )
                adjective = alliterate(noun, typ=NOUN)
        
    if adjective == None:
        print("eloquate '%s' nounonly result:" % (noun,),  noun )

        return noun
    elif random() &gt; 0.2:
        print("eloquate '%s' adj + noun result:" % (noun,), adjective + " " + noun )
        return adjective + " " + noun
    elif random() &gt; 0.5:
        print("eloquate '%s' noun + adj result:" % (noun,), noun + " " + adjective )
        return noun + " " + adjective
    else:
        print("eloquate '%s' noun so adj result:" % (noun,), noun + " so " + adjective )
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
        if old:
            word = en.verb.infinitive(word)
        else:
            word = en.verbs.conjugate(word, en.INFINITIVE)

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
<t tx="karstenw.20230227161027.1">allnouns = set( wordnet.NOUNS() )
allverbs = set( wordnet.VERBS() )
alladjectives = set( wordnet.ADJECTIVES() )

dictionary = []
stopwords = []
items = (
    ("vocabulary.txt", dictionary),
    ("stopwords.txt", stopwords) )
for item in items:
    path, container = item
    f = open(path, 'r', encoding="utf-8")
    for line in f.readlines():
        if not line:
            continue
        if line[0] in (" ", '#'):
            continue
        line = line.strip(" \n\r\t" )
        container.append( line )
    f.close()

dictionary = set( dictionary )
stopwords = set( stopwords )
dictionary = dictionary.difference( stopwords )

NOUN = "noun"
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
<t tx="karstenw.20230310124746.1">class FlowerWord:
    @others


</t>
<t tx="karstenw.20230310124806.1">def __init__(self, word):
    # pdb.set_trace()
    self.word = word
    self.synsets = wordnet.synsets( word )
    self.idx = 0
    self.antonym = ""
    self.gloss = ""
    self.synset = None
    if self.synsets:
        synonyms = self.synsets[0].synonyms
        try:
            self.idx = synonyms.index(word)
            self.synset = synonyms[self.idx]
        except:
            pass
        self.antonym = self.synsets[0].antonym
        self.gloss = self.synsets[0].gloss

</t>
<t tx="karstenw.20230310125018.1">def hyponyms(self):
    result = []
    for synset in self.synsets:
        hyponyms = synset.hyponyms()
        for hyponym in hyponyms:
            result.extend( hyponym.synonyms )
    result = list(set(result))
    return result

</t>
<t tx="karstenw.20230310134343.1">def printsynset( s ):
    print( '    synset:', s )
    print( '     gloss:', s.gloss )
    print( '  synonyms:', s.synonyms )
    print( '  hypernym:', s.hypernym )
    print( ' hypernyms:', s.hypernyms() )
    print( '  hyponyms:', s.hyponyms() )
    print( '  holonyms:', s.holonyms() )
    print( '  meronyms:', s.meronyms() )
    print( '   antonym:', s.antonym )
    print( '   lexname:', s.lexname )
    print( '    senses:', s.senses )
    print( '   similar:', s.similar() )

    print( '   _wnsynset._all_hypernyms:', s._wnsynset._all_hypernyms )
    print( '   _wnsynset._definition:', s._wnsynset._definition )
    print( '   _wnsynset._doc:', s._wnsynset._doc )
    print( '   _wnsynset._examples:', s._wnsynset._examples )
    print( '   _wnsynset._frame_ids:', s._wnsynset._frame_ids )

    print( '   _wnsynset._hypernyms:', s._wnsynset._hypernyms )
    print( '   _wnsynset._instance_hypernyms:', s._wnsynset._instance_hypernyms )
    print( '   _wnsynset._iter_hypernym_lists:', s._wnsynset._iter_hypernym_lists )
    print( '   _wnsynset._lemma_names:', s._wnsynset._lemma_names )
    print( '   _wnsynset._lemma_pointers:', s._wnsynset._lemma_pointers )
    print( '   _wnsynset._lemmas:', s._wnsynset._lemmas )
    print( '   _wnsynset._lexname:', s._wnsynset._lexname )
    print( '   _wnsynset._max_depth:', s._wnsynset._max_depth )
    print( '   _wnsynset._min_depth:', s._wnsynset._min_depth )
    print( '   _wnsynset._name:', s._wnsynset._name )
    print( '   _wnsynset._needs_root:', s._wnsynset._needs_root )
    print( '   _wnsynset._offset:', s._wnsynset._offset )
    print( '   _wnsynset._pointers:', s._wnsynset._pointers )
    print( '   _wnsynset._pos:', s._wnsynset._pos )
    print( '   _wnsynset._related:', s._wnsynset._related )
    print( '   _wnsynset._shortest_hypernym_paths:', s._wnsynset._shortest_hypernym_paths )
    print( '   _wnsynset._wordnet_corpus_reader:', s._wnsynset._wordnet_corpus_reader )
    print( '   _wnsynset.acyclic_tree:', s._wnsynset.acyclic_tree )
    print( '   _wnsynset.also_sees:', s._wnsynset.also_sees )
    print( '   _wnsynset.attributes:', s._wnsynset.attributes )
    print( '   _wnsynset.causes:', s._wnsynset.causes )
    print( '   _wnsynset.closure:', s._wnsynset.closure )
    print( '   _wnsynset.common_hypernyms:', s._wnsynset.common_hypernyms )
    print( '   _wnsynset.definition:', s._wnsynset.definition )
    print( '   _wnsynset.entailments:', s._wnsynset.entailments )
    print( '   _wnsynset.examples:', s._wnsynset.examples )
    print( '   _wnsynset.frame_ids:', s._wnsynset.frame_ids )
    print( '   _wnsynset.hypernym_distances:', s._wnsynset.hypernym_distances )
    print( '   _wnsynset.hypernym_paths:', s._wnsynset.hypernym_paths )
    print( '   _wnsynset.hypernyms:', s._wnsynset.hypernyms )
    print( '   _wnsynset.hyponyms:', s._wnsynset.hyponyms )
    print( '   _wnsynset.in_region_domains:', s._wnsynset.in_region_domains )
    print( '   _wnsynset.in_topic_domains:', s._wnsynset.in_topic_domains )
    print( '   _wnsynset.in_usage_domains:', s._wnsynset.in_usage_domains )
    print( '   _wnsynset.instance_hypernyms:', s._wnsynset.instance_hypernyms )
    print( '   _wnsynset.instance_hyponyms:', s._wnsynset.instance_hyponyms )
    print( '   _wnsynset.jcn_similarity:', s._wnsynset.jcn_similarity )
    print( '   _wnsynset.lch_similarity:', s._wnsynset.lch_similarity )
    print( '   _wnsynset.lemma_names:', s._wnsynset.lemma_names )
    print( '   _wnsynset.lemmas:', s._wnsynset.lemmas )
    print( '   _wnsynset.lexname:', s._wnsynset.lexname )
    print( '   _wnsynset.lin_similarity:', s._wnsynset.lin_similarity )
    print( '   _wnsynset.lowest_common_hypernyms:', s._wnsynset.lowest_common_hypernyms )
    print( '   _wnsynset.max_depth:', s._wnsynset.max_depth )
    print( '   _wnsynset.member_holonyms:', s._wnsynset.member_holonyms )
    print( '   _wnsynset.member_meronyms:', s._wnsynset.member_meronyms )
    print( '   _wnsynset.min_depth:', s._wnsynset.min_depth )
    print( '   _wnsynset.mst:', s._wnsynset.mst )
    print( '   _wnsynset.name:', s._wnsynset.name )
    print( '   _wnsynset.offset:', s._wnsynset.offset )
    print( '   _wnsynset.part_holonyms:', s._wnsynset.part_holonyms )
    print( '   _wnsynset.part_meronyms:', s._wnsynset.part_meronyms )
    print( '   _wnsynset.path_similarity:', s._wnsynset.path_similarity )
    print( '   _wnsynset.pos:', s._wnsynset.pos )
    print( '   _wnsynset.region_domains:', s._wnsynset.region_domains )
    print( '   _wnsynset.res_similarity:', s._wnsynset.res_similarity )
    print( '   _wnsynset.root_hypernyms:', s._wnsynset.root_hypernyms )
    print( '   _wnsynset.shortest_path_distance:', s._wnsynset.shortest_path_distance )
    print( '   _wnsynset.similar_tos:', s._wnsynset.similar_tos )
    print( '   _wnsynset.substance_holonyms:', s._wnsynset.substance_holonyms )
    print( '   _wnsynset.substance_meronyms:', s._wnsynset.substance_meronyms )
    print( '   _wnsynset.topic_domains:', s._wnsynset.topic_domains )
    print( '   _wnsynset.tree:', s._wnsynset.tree )
    print( '   _wnsynset.usage_domains:', s._wnsynset.usage_domains )
    print( '   _wnsynset.verb_groups:', s._wnsynset.verb_groups )
    print( '   _wnsynset.wup_similarity:', s._wnsynset.wup_similarity )


</t>
<t tx="karstenw.20230319115908.1">def hypernyms(self):
    result = []
    for synset in self.synsets:
        hypernyms = synset.hypernyms()
        for hypernym in hypernyms:
            result.extend( hypernym.synonyms )
        # hyponyms, antonym hypernyms
    result = list(set(result))
    return result

</t>
</tnodes>
</leo_file>
