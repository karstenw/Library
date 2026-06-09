# SIMILE

import pprint
pp=pprint.pprint

try:
    perception = ximport("perception")
except ImportError:
    perception = ximport("__init__")
    # reload(perception)

nouns = ("dog", "car", "cat", "mouse", "way", "summer", "winter",
         "queen", "king", "prince", "princess", "castle")


# Use Google search engine to look for properties:
q = choice( nouns )


results = perception.suggest_properties(q)
pp(results)
for property in results:
    count = "(" + str(results[property]) + ")"
    print(property, "is-property-of", q, count)
print()
