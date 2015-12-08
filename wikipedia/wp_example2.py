wikipedia = ximport("wikipedia")
 
result = wikipedia.search("food")
 
y = 100
for tag, txt in result.body:
 
  if tag == wikipedia.HEADING: 
    fontsize(16)
    y += 16
 
  if tag == wikipedia.PARAGRAPH: 
    fontsize(10)
 
  if tag == wikipedia.LIST:
    fontsize(10)
    txt = "* " + txt
 
  text(txt, 100, y, 600)
  y += textheight(txt, 600) * 1.1