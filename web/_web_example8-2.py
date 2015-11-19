# Definitions from the Urban Dictionary.

web = ximport("__init__")
reload(web)

definitions = web.urbandictionary.search("human")
text( choice(definitions), 50, 50, width=300)