# Wikipedia - last updated for NodeBox 1rc4
# Author: Tom De Smedt <tomdesmedt@trapdoor.be>
# Manual: http://nodebox.net/code/index.php/Wikipedia
# Copyright (c) 2006 by Tom De Smedt.
# Refer to the "Use" section on http://nodebox.net/code

from pywikipediabot import wikipedia as pywikipediabot
import sys

HEADING = "h1"
PARAGRAPH = "p"
LIST = "li"

class Output:

    """Mutes the output from print operations.

    No print commands are dumped when mute() is called.
    Used to filter comments from PyWikipediaBot we don't need.

    """

    def __init__(self): self.out = sys.stdout

    def mute(self): sys.stdout = self

    def on(self): sys.stdout = self.out

    def write(self, x): pass

class WikipediaError: pass
class WikipediaTimeout: pass

class WikipediaResult:
    
    def __init__(self, query):
        
        self.query = query
        self.url = ""
        self.body = ""
        self.links = []
        self.categories = []
        
        #Stop fetching content when nothing happens
        #for 30 seconds.
        import thread, time
        global thread_done
        thread_done = False
        start = time.time()
        thread.start_new_thread(self._fetch, (self.query,))
        while thread_done == False:
            time.sleep(1)
            if time.time() >= start+30:
                raise WikipediaTimeout

        self._parse()

    def _fetch(self, query):
    
        """Retrieves a query from Wikipedia.
    
        Retrieves a query using PyWikipediaBot to parse Wikipedia.
        PyWikipediaBot works "muted", without dumping any print messages.
    
        """
        
        global thread_done
    
        output = Output()
        output.mute()

        page = pywikipediabot.PageLink("en", query)
        if page.isRedirectPage():
            redirect = page.getRedirectTo()
            page = pywikipediabot.PageLink("en", str(redirect))

        try:
            self.query = query
            self.url = "http://en.wikipedia.org/wiki/" + page.urlname()
            self.body = page.get()
            self.links = page.links()
            output.on()
            thread_done = True
        
        except:
            output.on()
            raise WikipediaError
            thread_done = True

    def _replace_entities(self, string):

        """Replaces HTML special characters by readable characters.
    
        As taken from Leif K-Brooks algorithm on:
        http://groups-beta.google.com/group/comp.lang.python
        
        """

        import re 
        from htmlentitydefs import name2codepoint

        _entity_re = re.compile(r'&(?:(#)(\d+)|([^; ]+));') 

        def _repl_func(match):
            try:
                if match.group(1): # Numeric character reference 
                    return unichr(int(match.group(2))) 
                else: 
                    return unichr(name2codepoint[match.group(3)]) 
            except:
                return "?"

        return _entity_re.sub(_repl_func, string) 

    def _extract(self, string, start, stop):
        
        results = []
        i = string.find(start)
        while i >= 0:
            j = string.find(stop, i)
            results.append(string[i+len(start):j])
            string = string.replace(string[i:j+len(stop)], "")
            i = string.find(start, j-i)
            
        return string, results

    def _parse(self):

        """Parses the content from a wiki query.

        Removes all wiki formatting, tables, html-tags.
        Updates the body, list, url, in which
        body is a list of (tag, data) tuples,
        with tags: h1 (heading), p (paragraph) and li (list-items).
        The links value is a list of links found.

        Note: the first paragraph in a Wikipedia document usually
        (but not always) contains the most relevant/summarised information.

        """
        
        b = self.body
        #b = b.encode("utf-8")
        b = self._replace_entities(b)

        #Parse categories
        b, self.categories = self._extract(b, "[[Category:", "]]")

        #Remove wiki formatting
        hash = (
        ("[[",""), ("]]",""), ("[",""), ("]",""), ("|","/"),
        ("''",""), ("'''",""),
        ("{/", "{{"), ("/}", "}}"),
        ("----", ""),
        ("External links","Hyperlinks"),
        ("simple:"+self.query.capitalize(),"")
        )
        for x,y in hash: b = b.replace(x, y)

        #Remove wiki and html tables
        b = b.replace("<table>", "{{<table>")
        b = b.replace("</table>", "</table>}}")
        b, x = self._extract(b, "{{", "}}")
        b = b.replace("}\n}", "}}")
        b = b.replace("}}}", "")
        b = b.replace("}}", "")

        ##Remove any html tags
        b, x = self._extract(b, "<", ">")

        #Commit each line in body to list
        list = [(HEADING, self.query.capitalize())]
        b = b.split("\n")
    
        p = ""
        for line in b:
            line = line.strip("\r").strip()
            #Add previous paragraph and heading
            if line.find("==") == 0:
                if len(p) > 0 : list.append((PARAGRAPH, p))
                list.append((HEADING, line.strip("=").strip()))
                p = "" 
            #Add previous paragraph and list-item
            elif line.find("*") == 0:
                if len(p) > 0 : list.append((PARAGRAPH, p))
                list.append((LIST, line.strip("*").strip()))
                p = ""
            #Treat indents like paragraphs
            elif line.find(":") == 0:
                if len(p) > 0 : list.append((PARAGRAPH, p))
                list.append((PARAGRAPH, line.strip(":").strip()))
                p = ""  
            #Ignore wiki language links
            elif line.find(":") == 2:
                pass          
            #Ignore image links
            elif line.lower().find("image:") >= 0:
                pass          
            #Add previous paragraph   
            elif line == "":
                if len(p) > 0 : list.append((PARAGRAPH, p))
                p = ""               
            else:
                p += line            
        if len(p) > 0 : list.append((PARAGRAPH, p))

        self.body = list

        #Commit links to list
        list = []
        for link in self.links:
            #link = link.encode("utf-8")
            link = self._replace_entities(link)
            #Ignore wiki image links
            if link.lower().find("image:") < 0:
                list.append(link)

        self.links = list

def search(query):
    
    """Searches and parses Wikipedia for query.
    
    Searches Wikipedia using PyWikipediaBot.
    Returns a WikipediaResult object, in which
    body is a tagged list of strings, for example:
    [(HEADING,"Title"), (PARAGRAPH,"A paragraph of text.")].

    """
    
    return WikipediaResult(query)