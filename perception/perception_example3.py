# SIMILE

import pprint
pp=pprint.pprint

try:
    perception = ximport("perception")
except ImportError:
    perception = ximport("__init__")
    # reload(perception)

# Use Google search engine to look for properties:
q = "queen"
results = perception.suggest_properties(q)
# print("\n\nresults:", results)
for property in results:
    count = "(" + str(results[property]) + ")"
    print(property, "is-property-of", q, count)
print()
