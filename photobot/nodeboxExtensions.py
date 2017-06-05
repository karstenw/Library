
"""This is a collection of functions which extend NodeBox since v1.9.17+

By importin * from here these can be used in older NodeBoxes...
"""
import os
import datetime
import unicodedata

import objc
import Foundation

__all__ = ('filelist', 'imagefiles', 'datestring', 'makeunicode')


### Utilities ###

def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    typ = type(s)
    
    # convert to str first; for number types etc.
    if typ not in (str, unicode):
        s = str(s)
    if typ not in (unicode, Foundation.NSMutableAttributedString, objc.pyobjc_unicode,
                   Foundation.NSMutableStringProxyForMutableAttributedString):
        try:
            s = unicode(s, srcencoding)
        except TypeError, err:
            print 
            print "makeunicode():", err
            print repr(s)
            print type(s)
            #pdb.set_trace()
            print
    if typ in (unicode,):
        s = unicodedata.normalize(normalizer, s)
    return s


def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
    """Make an ISO datestring. The defaults are good for using the result of
    'datestring()' in a filename.
    """
    if not dt:
        now = str(datetime.datetime.now())
    else:
        now = str(dt)
    if not dateonly:
        now = now[:19]
    else:
        now = now[:10]
    if nospaces:
        now = now.replace(" ", "_")
    if nocolons:
        now = now.replace(":", "")
    return now


def filelist( folderpathorlist, pathonly=True ):
    """Walk a folder or a list of folders and return
    paths or ((filepath, size, lastmodified, mode) tuples..
    """

    folders = folderpathorlist
    if type(folderpathorlist) in (str, unicode):
        folders = [folderpathorlist]
    result = []
    for folder in folders:
        for root, dirs, files in os.walk( folder ):
            root = makeunicode( root )

            for thefile in files:
                thefile = makeunicode( thefile )
                basename, ext = os.path.splitext(thefile)

                # exclude dotfiles
                if thefile.startswith('.'):
                    continue

                # exclude the specials
                for item in (u'\r', u'\n', u'\t'):
                    if item in thefile:
                        continue

                filepath = os.path.join( root, thefile )

                record = filepath
                if not pathonly:
                    info = os.stat( filepath )
                    lastmodified = datetime.datetime.fromtimestamp( info.st_mtime )
                    record = (filepath, info.st_size, lastmodified, oct(info.st_mode) )
                yield record


def imagefiles( folderpathorlist, pathonly=True ):

    result = []
    filetuples = filelist( folderpathorlist, pathonly=pathonly )
    # extensions = tuple(".pdf .eps .tif .tiff .gif .jpg .jpeg .png".split())
    extensions = tuple(".pdf .eps .tif .tiff .gif .jpg .jpeg .png".split())
    for filetuple in filetuples:
        path = filetuple
        if not pathonly:
            path = filetuple[0]
        _, ext = os.path.splitext( path )
        if ext.lower() not in extensions:
            continue
        if pathonly:
            yield path
        else:
            yield filetuple

