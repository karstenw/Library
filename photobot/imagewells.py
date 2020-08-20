import sys
import os
import datetime
import unicodedata

import fractions
Fraction = fractions.Fraction


import PIL
import PIL.Image as Image



__all__ = ['imagewells', 'loadImageWell']


def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    typ = type(s)
    
    # convert to str first; for number types etc.
    if typ not in (str, unicode):
        s = str(s)
    if typ not in (unicode, ):
        try:
            s = unicode(s, srcencoding)
        except TypeError, err:
            print "makeunicode():", err
            print type(s), repr(s)
    if typ in (unicode,):
        s = unicodedata.normalize(normalizer, s)
    return s


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
                    lastmodf = datetime.datetime.fromtimestamp( info.st_mtime )
                    islink = os.path.islink( filepath )
                    record = (filepath,
                              info.st_size,
                              lastmodf,
                              oct(info.st_mode),
                              islink )
                yield record


def imagefiles( folderpathorlist, pathonly=True ):
    """Get a list of images from a list of folders.

    folderpathorlist: is either a string with a path or a list of paths
    
    pathonly: if True return list of fullpath
              else: return a list of filetuples
    filetuple = 
        (path, filesize, lastmodf, mode, islink, width, height)
    
    """
    filetuples = filelist( folderpathorlist, pathonly=pathonly )
    exts = ".tif .tiff .gif .jpg .jpeg .png" # + " .eps"
    extensions = tuple( exts.split() )
    for filetuple in filetuples:
        path = makeunicode( filetuple )
        if not pathonly:
            path = filetuple[0]

        _, ext = os.path.splitext( path )
        if ext.lower() not in extensions:
            continue
        if pathonly:
            yield path
        else:
            path, filesize, lastmodf, mode, islink = filetuple
            s = (-1,-1)
            try:
                img = Image.open(path)
                s = img.size
                del img
            except:
                pass #continue
            filetuple = (path, filesize, lastmodf, mode, islink, s[0], s[1])
            yield filetuple


#
# image well
#

def imagewells():
    """Find a file named "imagewell.txt" and interpret it as image folder paths.
    If no file is found create one with the desktop image folders for
    mac & win10.
    
    """
    folders = ["/Library/Desktop Pictures", "C:\Windows\Web" ]
    images = os.path.abspath( "images" )
    if os.path.exists( images ):
        folders.append( images )
    fullpath = os.path.abspath( "imagewell.txt" )
    
    if not os.path.exists( fullpath ):
        try:
            f = open(fullpath, 'w')
            f.write( "\n".join( folders ) )
            f.close()
        except:
            pass
        return folders
    try:
        with open(fullpath, 'Ur') as f:
            lines = f.readlines()
        if not lines:
            return folders
        folders = []
        for line in lines:
            line = line.strip("\n\r")
            folders.append( makeunicode( line ) )
    except:
        pass
    folders = [x for x in folders if os.path.exists(x)]
    return folders


def loadImageWell( bgsize=(1024,768), minsize=(256,256),
                   maxfilesize=100000000, maxpixellength=16000,
                   pathonly=True, additionals=None, ignorelibs=False):
    """Find images imagewells or additional folders. 
       
        Params:
            bgsize - tuple with width and height for images to be classified background
            minsize - tuple with minimal width and height for images not to be ignored
            maxfilesize - in bytes. Images above this file size will be ignored
            maxpixellength - in pixels. Images above in either dimension will be ignored
            pathonly - return path or record
            additionals - list of folders to me considered for this run
            ignorelibs - if imagewells file should be ignored
    
        Returns:
            A dict of dicts with several image classifications.
            
            

            list of file paths if pathonly is True
            list of file records else.
            
            
    
    
    """


    # get all images from user image wells
    folders = []
    if not ignorelibs:
        folders = imagewells()
    
    if additionals:
        folders.extend( additionals )
    filetuples = imagefiles( folders, pathonly=False )

    tiles = []
    backgrounds = []
    proportions = {}
    fractions = {}

    result = {
        'allimages': [],
        'tiles': [],
        'backgrounds': [],
        'landscape': [],
        'portrait': [],
        'fractions': {}
    }

    minw, minh = minsize
    bgw, bgh = bgsize
    for t in filetuples:
        path, filesize, lastmodified, mode, islink, w0, h0 = t
        folder, filename = os.path.split( path )
        basename, ext = os.path.splitext( filename )

        # filter min & max pixel sizes
        if ext.lower() != ".eps":
            if (w0 < minw) and (h0 < minh):
                continue
            if (w0 > maxpixellength) or (h0 > maxpixellength):
                continue
        
        # filter max filesize
        if filesize > maxfilesize:
            continue

        # set proportion name and fraction
        proportion = "landscape"
        if h0 > w0:
            proportion = "portrait"
        try:
            frac = Fraction(w0, h0)
        except TypeError, err:
            print err
            print w0
            print h0

        if pathonly:
            record = path
        else:
            record = (path, filesize, lastmodified, mode, islink,
                      w0, h0, proportion, frac)

        # candidate has at least canvas size and can be used as background
        result['allimages'].append( record )
        if w0 >= bgw and h0 >= bgh:
            result['backgrounds'].append( record )
        else:
            result['tiles'].append( record )
        
        if frac not in result['fractions']:
            result['fractions'][frac] = []

        result['fractions'][frac].append( record )
        if proportion == "landscape":
            result['landscape'].append( record )
        else:
            result['portrait'].append( record )
    return result


