# Copyright (c) 2015 Karsten Wolf

# switched to using imagesnap

# since it's based on the old isight library, the same LICENCE applies.
# See LICENSE.txt for details.

import os
import shutil


def grab(destfolder=False):


    # a hardcoded hack :-(
    filename = "NdBx-00000.jpg"

    """ Calls Robert Harder's command line tool for the iSight
    and returns a list of paths where the image is located.
    http://iharder.net/imagesnap
    """
    
    me = os.path.abspath(__file__)
    cmdpath = os.path.split( me )[0]
    print cmdpath
    arg0  = os.path.join(cmdpath, "imagesnap")

    path = destfolder
    if not destfolder:
        path = cmdpath

    destpath = os.path.join(path, filename)

    cmd = '''"%s" -v -p "%s" filename''' % (arg0, path)

    os.system(cmd)

    return destpath


def grabSequence(count=10, intervall=0.1, destfolder=False): #, emptyFolder=False):
    """Grabs count images from the isight taken with interval deltaT
    
    - destfolder may be the path to a destination folder where the images
      will be stored. if not given, 
    
    - emptyfolder deactivated for now. The idea is to delete the folder
      right before the grab runs. Currently the default destfolder just grows...

    Returns a list of paths which can be iterated and fed to image()
    """
    me = os.path.abspath(__file__)
    cmdpath = os.path.split( me )[0]
    print cmdpath
    arg0  = os.path.join(cmdpath, "imagesnap")
    
    userimagefolder = os.path.join( os.path.abspath( os.path.expanduser("~")),
                                    "Pictures",
                                    "Nodebox-iSight-Sequences")

    if destfolder:
        destfolder = os.path.abspath( os.path.expanduser( destfolder ))

    folder = destfolder

    if not destfolder:
        folder = userimagefolder

    # empty dir from previous run
    """
    if emptyFolder:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
    """

    # ask for existence, the previous command could have aborted
    if not os.path.exists(folder):
        os.makedirs(folder)

    cmd = '''"%s" -v -n %i -t %f -p "%s"''' % (arg0, count, intervall, folder)

    os.system(cmd)
    
    # print cmd

    result = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if name.startswith("NdBx"):
                result.append( os.path.join(root, name) )
    result.sort()

    # filter last count images
    if len( result) > count:
        result = result[-count:]
    return result
