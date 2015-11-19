import os
import pdb

def grab(width=320, height=240,
         nativesize=False, destfolder=False):


    # a hardcoded hack :-(
    filename = "NdBx-0000.jpg"

    """ Calls Robert Harder's command line tool for the iSight
    and returns a list of paths where the image is located.
    http://iharder.net/imagesnap
    """
    
    cmdpath = os.path.abspath('.')
    arg0  = os.path.join(cmdpath, "imagesnap")

    path = destfolder
    if not destfolder:
        path = cmdpath

    destpath = os.path.join(path, filename)

    cmd = '''"%s" -v -p "%s" filename''' % (arg0, path)

    os.system(cmd)

    return destpath



def grabSequence(count=10, intervall=0.66, destfolder=False, emptyFolder=False):

    cmdpath = os.path.abspath('.')
    arg0  = os.path.join(cmdpath, "imagesnap")

    if destfolder:
        destfolder = os.path.abspath( os.path.expanduser( destfolder ))
    folder = destfolder
    if not destfolder:
        folder = os.path.join(cmdpath, "sequence")

    # empty dir from previous run
    if emptyFolder:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    # ask for existence, the previous command could have aborted
    if not os.path.exists(folder):
        os.makedirs(folder)

    cmd = '''"%s" -v -n %i -t %f -p "%s"''' % (arg0, count, intervall, folder)

    os.system(cmd)

    result = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if name.startswith("NdBx"):
                result.append( os.path.join(root, name) )
    result.sort()
    return result

#s = grabSequence()
#print "RETURN:", s
destfolder = os.path.expanduser( "~/Desktop" )

imagepaths = grab( destfolder=destfolder )
print imagepaths

