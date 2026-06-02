import pdb
import pprint
pp=pprint.pprint

# Print out the en.wikipedia sections names for "cat"

import linguistics
import pattern
from pattern.web import Wikipedia

# import wikipedia
engine = Wikipedia(language="en")

article = Wikipedia().search( 'cat' )

for section in article.sections:
    print( '  ' * section.level + section.title )

