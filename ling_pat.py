
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""


import sys,os,pprint,pdb,time
pp=pprint.pprint

s1 = time.time()
import linguistics

s2 = time.time()
print("import linguistics %.3f" % (s2-s1) )

import pattern
import pattern.en

import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = en.wordnet

if 0:
    from pattern.en import article, referenced
    from pattern.en import pluralize, singularize
    from pattern.en import comparative, superlative
    from pattern.en import conjugate, lemma, lexeme, tenses

    from pattern.en import NOUN, VERB, ADJECTIVE, DEFINITE, INDEFINITE
    from pattern.en import INDICATIVE, IMPERATIVE, CONDITIONAL, SUBJUNCTIVE
    from pattern.en import SINGULAR, PLURAL

    from pattern.text import IMPERFECTIVE, PERFECTIVE, PROGRESSIVE
    from pattern.text import INFINITIVE, PRESENT, PAST, FUTURE



s3 = time.time()
print("import pattern %.3f" % (s3-s2) )


# pdb.set_trace()

theword = "house"
theverb = "walk"

synsets = wordnet.synsets( theword )
print()
print()
s = synsets[0]
print( '    synset:', s )
print( '     gloss:', s.gloss )
print( '    senses:', s.senses )
print( '  synonyms:', s.synonyms )
print( '   antonym:', s.antonym )
print( '   lexname:', s.lexname )

print(  )
print( ' Hypernyms:', s.hypernyms() )
print( '  Hyponyms:', s.hyponyms() )
print( '  Holonyms:', s.holonyms() )
print( '  Meronyms:', s.meronyms() )
print()

s4 = time.time()
print("synset demo %.3f" % (s4-s3) )

print()

print("article:", pattern.en.article( theword, function=pattern.en.INDEFINITE ) )
print("referenced:", pattern.en.referenced( theword, article=pattern.en.INDEFINITE ) )

print()

print("lemma: ", pattern.en.lemma(theverb) )
print("lexeme: ", pattern.en.lexeme(theverb) )
print("tenses: ")
pp( pattern.en.tenses(theverb) )


if 0:
    print("conjugate: ", theverb )
    for tense in (pattern.text.INFINITIVE, pattern.text.PRESENT,
                  pattern.text.PAST, pattern.text.FUTURE):
        for person in (1,2,3,None):
            for number in (pattern.en.SINGULAR, pattern.en.PLURAL):
                for mood in (pattern.en.INDICATIVE, pattern.en.IMPERATIVE,
                             pattern.en.CONDITIONAL, pattern.en.SUBJUNCTIVE):
                    for aspect in (pattern.text.IMPERFECTIVE,
                                   pattern.text.PERFECTIVE,
                                   pattern.text.PROGRESSIVE):
                        for negated in (True, False):
                            c = pattern.en.conjugate( theverb, tense, person,
                                                      number, mood, aspect, negated, True)
                            print(c)


if 1:
    allnouns = set( wordnet.NOUNS())
    misses = {}
    for noun in allnouns:
        ss = wordnet.synsets( noun )[0]
        if ss.synonyms[0] != noun:
            if noun in ss.synonyms:
                continue
            lower = [t.lower() for t in ss.synonyms]
            if noun in lower:
                continue
            if noun not in misses:
                misses[noun] = []
            misses[noun].extend( ss.synonyms )
    print("##misses:", len(misses) )

    s5 = time.time()
    print("check all synsets %.3f" % (s5-s4) )

