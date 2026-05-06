import pprint
pp=pprint.pprint

import imagewells
loadImageWell = imagewells.loadImageWell

imagewell = loadImageWell()

for key in imagewell:
    print("  %s:   %i" %(key, len(imagewell[key])))

