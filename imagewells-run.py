import pprint
pp=pprint.pprint

import imagewells
imagewell = imagewells.loadImageWell()

for key in imagewell:
    print("  %s:   %i" %(key, len(imagewell[key])))
pp( imagewell["allimages"], width=240 )        
print()
