# Reading newsfeeds.

try:
    web = ximport("web")
except:
    web = ximport("__init__")
    reload(web)

# Get a random URL from our favorites list.
url = choice(web.newsfeed.favorites.values())

print "URL", url

# Parse the newsfeed data into a handy object.
feed = web.newsfeed.parse(url)

# Get the title and the description of the feed.
fontsize(20)

t = str(feed.title) + ": " + str(feed.description)
text(t, 20, 20 , width=600)

fontsize(10)

s = u""

for item in feed.items:
    #print "-" * 40
    #print "- Title       :", item.title
    #print "- Link        :", item.link
    #print "- Description :", web.html.plain(item.description)
    #print "- Date        :", item.date
    #print "- Author      :", item.author
    if item.description:
        s = s + unicode(item.description)
text(s, 20, 40, width= 600) 
# fontsize(10)

# print item.description
# text(item.description, 20, 20, width=200)
