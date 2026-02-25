# Note: you'll also need the NodeBox English Linguistics library:
# http://nodebox.net/code/index.php/Linguistics

try:
    flowerewolf = ximport("flowerewolf")
except:
    flowerewolf = ximport("__init__")
    reload(flowerewolf)

var("topic", TEXT, "kiss")
size(600,700)

fontsize(16)
fonts = ["Georgia-Bold", "Helvetica", "ArialNarrow"]
flowerewolf.dada(str(topic), 
     foreground=color(1,1,1), 
     background=color(1,0,0), 
     fonts=fonts)