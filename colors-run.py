
import sys, os, pdb, pprint
pp=pprint.pprint

import colors

# pdb.set_trace()

# Our own theme of ancient colors:
t = colors.theme( "babylonia" )
# t.name = "babylonia"
t.add_range(colors.soft, colors.ivory(), 0.5)
t.add_range(colors.dark, colors.darkgoldenrod(), 0.2)
t.add_range(colors.intense, colors.gold(), 0.2)
t.add_range(colors.warm, colors.brown(), 0.2)
t.add_range(colors.neutral, colors.teal(), 0.1)
t.add_range(colors.intense, colors.red(), 0.1)

## ancient egypt + love = ancient eve!
t2 = colors.aggregate("love")
t = t.recombine(t2)
print( t.name )

#stroke(0)
#strokewidth(0.2)
#t.swatch(50,50,n=12, grouped=False)

