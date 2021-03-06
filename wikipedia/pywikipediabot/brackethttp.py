"""
Script to correct URLs like
(http://www.example.org) to [http://www.example.org example.org]
to have correct generation of links in Wikipedia
"""
#
# (C) 2003 Thomas R. Koll, <tomk32@tomk32.de>
#
# Distribute under the terms of the PSF license.
#
__version__='$Id: brackethttp.py,v 1.3 2003/12/14 08:59:26 hooft Exp $'
#
import re, sys

import wikipedia

myComment = 'Bot: URL fixed'

for arg in sys.argv[1:]:
    if wikipedia.argHandler(arg):
        pass
    else:
        pl = wikipedia.PageLink(wikipedia.mylang, arg)
        text = pl.get()
        
        newText = re.sub("(http:\/\/([^ ]*[^\] ]))\)", "[\\1 \\2])", text)

        if newText != text:
            import difflib
            for line in difflib.ndiff(text.split('\r\n'),newText.split('\r\n')):
                if line[0] in ['+','-']:
                    print repr(line)[2:-1]
            status, reason, data = pl.put(newText, myComment)
            print status, reason
        else:
            print "No bad link found"
