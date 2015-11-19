try:
    cornu = ximport("cornu")
except:
    cornu = ximport("__init__")
    reload(cornu)

size(600,600)

var("x1", NUMBER, 0.2, 0.0, 1.0)
var("y1", NUMBER, 0.2, 0.0, 1.0)
var("x2", NUMBER, 0.2, 0.0, 1.0)
var("y2", NUMBER, 0.4, 0.0, 1.0)
var("x3", NUMBER, 0.3, 0.0, 1.0)
var("y3", NUMBER, 0.3, 0.0, 1.0)
var("x4", NUMBER, 0.5, 0.0, 1.0)
var("y4", NUMBER, 0.6, 0.0, 1.0)
var("tweaks", NUMBER, 10, 0, 20)

stroke(0)
nofill()
cornu.drawpath([(x1,y1), (x2,y2), (x3,y3), (x4,y4)], tweaks=int(tweaks), points=True)