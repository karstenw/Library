"""This is a minimal script to parse an XML file such as the sax_parse_bug.dat
dumps that interwiki.py can make if something fails. The only goal of this
program is to get a stack trace listing line number and column of the invalid
character in the XML.

Pass this script the name of an XML file as argument.
"""
#
# (C) Rob W.W. Hooft, 2003
#
# Distribute under the terms of the PSF license.
#
__version__ = '$Id: xmltest.py,v 1.1 2003/12/20 09:38:42 hooft Exp $'
#
import sys, xml.sax, xml.sax.handler

h = xml.sax.handler.ContentHandler()
xml.sax.parse(open(sys.argv[1], 'r'), h)

