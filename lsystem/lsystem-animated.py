# by mark meyer | http://www.photo-mark.com | enjoy. 
size(800, 800)
speed(24)
colormode(RGB)

segmentLength = 300
rightTurnAngle = 180 
leftTurnAngle =  180


def setup():
    pass

def draw():
    global leftTurnAngle, rightTurnAngle
    background(0.25,0.0,0.1)
    strokewidth(3)
    stroke(1, 1, 0, .65)
    nofill()

    translate(400, 500) #starting point


    rules= {}
    ##  The symbold for the formal language are: 
    #       [ = save state (i.e push()).  ] = restore state (i.e. pop()). 
    #       + and - = turn right and left respectively (based on angles given above)
    #       Other symbolds are recursively substituted and then processed as a draw forward instruction
    rules['w'] = 'A' # This is the starting rule
    rules['A'] = 'B+A+B'
    rules['B'] = 'A-B-A'
    iterations = 5 # Be careful with large numbers of iterations--the complexity grows exponentially

    def mydraw():
        beginpath(0, 0)
        lineto(0, -segmentLength)
        endpath()
        transform(mode=CORNER)
        translate(0, -segmentLength)
    
    def iterate(n, rule):
        if rule == '+':
            rotate(rightTurnAngle)
            return
        elif rule == '-':
            rotate(leftTurnAngle)
            return
        elif rule == "[": 
            push()
            return
        elif rule == "]":
             pop()
             return
        if n > 0:
            # scaling on each iteration is fun to play with
            for step in rules[rule]:
                #scale(.99)
                iterate(n-1, step)
        else: 
            mydraw()
    
    iterate(iterations, 'w')
    leftTurnAngle -= 1
    rightTurnAngle -=1
