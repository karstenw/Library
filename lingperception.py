
import sys,os,pprint,pdb,time
pp=pprint.pprint

#s1 = time.time()
#import linguistics
s2 = time.time()

import perception

# pdb.set_trace()
# q = perception.cluster("cool", depth=2, max=30, labeled=False)
s3 = time.time()
print( "import perception: %.4fs" % (s3 - s2) )
print( "import perception internal: %.4fs" % (perception.stopimport - perception.startimport) )

# concepts, edges, loadedConcepts = perception.query( "cool" )

rules = perception.query( "cool" )

s4 = time.time()
print( "query cool: %.4fs" % (s4 - s3) )


pp( rules )
# print( edges )
