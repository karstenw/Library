# SIMILE
from __future__ import print_function

try:
    perception = ximport("perception")
except ImportError:
    perception = ximport("__init__")
    reload(perception)

# Use Google search engine to look for properties:
q = "queen"
results = perception.suggest_properties(q)
print("results:", results)
for property in results:
    count = "(" + str(results[property]) + ")"
    print(property, "is-property-of", q, count)