
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""


import pdb
import pprint
pp=pprint.pprint

import linguistics
import pattern
from pattern.web import Wikipedia

engine = Wikipedia(language="en")

# article = engine.search("list of terrorist incidents", cached=True)
article = engine.search("david bowie", cached=True)


# pdb.set_trace()

if 1:
    for item in (
        #'_plaintext', 'categories', 'disambiguation',
        # 'download',
        'external',
        # 'html', 'language', 'languages',
        # 'links', 'media',
        'parser',
        # 'plaintext',
        'query',
        'redirects', 'sections',
        # 'source', 'src', 'string',
        'title'):
        f = article.__getattribute__(item)
        s = f
        try:
            if '__call__' in dir(f):
                print(item,"()", ':' )
                s = f()
            else:
                print(item, ':' )

        except Exception as err:
            s = err
        print("--" * 40 )
        pp( s, width=260 )
        print("\n\n")
    print("--" * 40 )


print(article.title)            # Article title (may differ from the search query).
print("")

print("Links")
for i, link in enumerate(article.links):
    print( "link:", link )
print("")

print("disambiguation:", article.disambiguation)
print()

print("categories:")
pp(article.categories)
print()

print("media:")
pp(article.media)
print()

print("language:", article.language)
print("languages:")
pp(article.languages)
print()

print("sections:")
for section in article.sections:
    print( str(' ' * section.level + section.title) )
# pp(article.sections)
print()


# Article in French, can be retrieved with Wikipedia(language="fr").
print("article in FR:", article.languages["fr"])
print("links:")
pp(article.links)       # List of linked Wikipedia articles.

print("external:")
pp(article.external)     # List of external URL's.
print("")

nodes = []
relevant = False
previous = ""


#pp( dir(article) )
#pp( article )

# pdb.set_trace()
if 0:
    for tag, p in body:
        if p == "2000s":
            relevant = True
        if p == "See also": relevant = False
        if relevant: 
            p = p.replace("\"", "'")
            nodes.append("")
            previous = p

if 0:
    font("Arial")
    fontsize(8)
    lineheight(0.8)
 
    import network
    xml = "\n".join(nodes)
    network.map(xml, 0, 0, WIDTH, HEIGHT, radius=100)
