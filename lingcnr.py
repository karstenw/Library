import sys
import os
import pprint
pp=pprint.pprint
import pdb
from pathlib import Path

import linguistics

import linguistics.conceptnetreader
cnr = linguistics.conceptnetreader

if 1:
    print( "cnr.databasefile:", cnr.databasefile )

    print( "#languages:", len(cnr.languages) )
    print( "#relations:", len(cnr.relations) )
    print( "#contexts:", len(cnr.contexts) )
    # pp( cnr.relations )

