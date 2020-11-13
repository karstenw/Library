wordnet = ximport("wordnet")

from wordnet import explode

try:
    font("Georgia-BoldItalic", 12)
    # font("Times New Roman", 16)
except:
    pass

fill(0.3)

q = "berth"

explode.draw(q, wordnet.noun_hyponyms(q), 450, 450, max=50)
