<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20230615120047.2" a="E"><vh>Ants</vh>
<v t="karstenw.20230615120112.1"><vh>@clean __init__.py</vh>
<v t="karstenw.20230615120123.1"><vh>Declarations</vh></v>
<v t="karstenw.20230615120123.2"><vh>class Food</vh>
<v t="karstenw.20230615120123.3"><vh>__init__</vh></v>
</v>
<v t="karstenw.20230615120123.4"><vh>class Pheromone</vh>
<v t="karstenw.20230615120123.5"><vh>__init__</vh></v>
<v t="karstenw.20230615120123.6"><vh>evaporate</vh></v>
</v>
<v t="karstenw.20230615120123.7"><vh>class Ant</vh>
<v t="karstenw.20230615120123.8"><vh>__init__</vh></v>
<v t="karstenw.20230615120123.9"><vh>near</vh></v>
<v t="karstenw.20230615120123.10"><vh>goal</vh></v>
<v t="karstenw.20230615120123.11"><vh>wander</vh></v>
<v t="karstenw.20230615120123.12"><vh>follow</vh></v>
<v t="karstenw.20230615120123.13"><vh>harvest</vh></v>
<v t="karstenw.20230615120123.14"><vh>hoard</vh></v>
<v t="karstenw.20230615120123.15"><vh>forage</vh></v>
</v>
<v t="karstenw.20230615120123.16"><vh>class Colony</vh>
<v t="karstenw.20230615120123.17"><vh>__init__</vh></v>
</v>
<v t="karstenw.20230615120123.18"><vh>colony</vh></v>
<v t="karstenw.20230615120123.19"><vh>food</vh></v>
</v>
<v t="karstenw.20230615120224.1" a="E"><vh>@clean ants_example.py</vh>
<v t="karstenw.20230615120243.1"><vh>Declarations</vh></v>
<v t="karstenw.20230615120243.2"><vh>setup</vh></v>
<v t="karstenw.20230615120243.3"><vh>draw</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230615120047.2"></t>
<t tx="karstenw.20230615120112.1">@language python
@tabwidth -4
@others
if __name__=='__main__':
    c = colony(30, 0, 0, 100)
    c.foodsources.append(food(50, 50, 50))
    for i in range(5):
        for ant in c:
            from pudb import set_trace; set_trace()
            ant.forage()
            print( ant.x, ant.y )

</t>
<t tx="karstenw.20230615120123.1"># Ants - last updated for NodeBox 1.9.1
# Author: Tom De Smedt &lt;tomdesmedt@organisms.be&gt;
# Copyright (c) 2007 Tom De Smedt.
# See LICENSE.txt for details.

from __future__ import print_function

from random import random, randint, uniform

</t>
<t tx="karstenw.20230615120123.10">def goal(self, obj):
    
    """Set a goal to move towards.
    
    Sets the object, which has x and y properties, as goal.
    The ant starts moving towards it.
    
    """
    
    self.vx = (obj.x-self.x) / abs(obj.x-self.x+0.0001)
    self.vy = (obj.y-self.y) / abs(obj.y-self.y+0.0001)
    
    try:
        self.vy /= abs(obj.x-self.x) / abs(obj.y-self.y+0.0001) #w to h ratio
    except ZeroDivisionError:
        pass
    
    self.wandering = 0

</t>
<t tx="karstenw.20230615120123.11">def wander(self, d=0.3):
    
    """Wander around randomly.
    
    Ants wander around randomly until they find food.
    The d parameter controls the chaos with which the ant moves:
    a higher d means a more erratic ant,
    but too high is inefficient as the ant becomes indecisive.
    
    Eventually, ants that have been doing nothing to long,
    return to the colony.
    
    """
    
    self.vx += uniform(-d, d)
    self.vy += uniform(-d, d)
    
    self.wandering += 1
    if self.wandering &gt; self.colony.r: self.goal(self.colony)
    if self.near(self.colony): self.wandering = 0

</t>
<t tx="karstenw.20230615120123.12">def follow(self):
    
    """Follow a nearby pheromone trail.
    
    If the ant is not carrying food to the colony,
    follow any nearby trail.
    If the pheromone has evaporated to much,
    the ant might lose interest in the trail,
    this ensures it doesn't get "stuck" on a useless trail.
    
    """
    
    for ant in self.colony:
        if ant != self or self.has_food == False:
            for pheromone in ant.trail:
                if self.near(pheromone):
                    if random() &gt; pheromone.strength: return
                    self.goal(pheromone)
                    if pheromone.strength &gt; 0.5: return
                    else: break

</t>
<t tx="karstenw.20230615120123.13">def harvest(self):
    
    """Collect nearby food.
    
    If the ant is not carrying anything,
    and it is near a source of food,
    pick up food and start marking the trail home.
    
    """

    for food in self.colony.foodsources:
        if self.near(food, radius=max(2,food.size/2)) and self.has_food == False: 
            food.size -= 1
            if food.size == 0: self.colony.foodsources.remove(food)
            self.trail = [Pheromone(food.x, food.y)]
            self.trail.append(Pheromone(self.x, self.y))
            self.has_food = True
    
</t>
<t tx="karstenw.20230615120123.14">def hoard(self, trail=0.5):
    
    """Return straight home with food.
    
    Leave a trail of pheromone markers,
    which the other ants smell and follow to the food.
    
    """
    
    if self.has_food:
        self.goal(self.colony)
        if random() &lt; trail:
            self.trail.append(Pheromone(self.x, self.y))
    
    #Drop food and start wandering again
    if self.near(self.colony) and self.has_food:
        self.trail.append(Pheromone(self.colony.x, self.colony.y))
        self.vx = 0
        self.vy = 0
        self.has_food = False
        self.colony.food += 1

</t>
<t tx="karstenw.20230615120123.15">def forage(self, speed=2):
    
    self.follow() #follow nearby trails to food.
    self.harvest() #harvest nearby food source
    self.hoard() #bring food directly to colony
    self.wander() #some random wandering is more efficient

    self.vx = max(-speed, min(self.vx, speed))
    self.vy = max(-speed, min(self.vy, speed))        
    
    self.x += self.vx
    self.y += self.vy
    
    #trail evaporation
    for pheromone in self.trail:
        pheromone.evaporate()
        if pheromone.strength == 0:
            self.trail.remove(pheromone)

</t>
<t tx="karstenw.20230615120123.16">class Colony(list):
    
    @others
</t>
<t tx="karstenw.20230615120123.17">def __init__(self, n, x, y, r):
    
    self.foodsources = []
    self.food = 0
    
    for i in range(n):
        self.append(Ant(self, x, y))
                         
    self.x = x
    self.y = y
    self.r = r

</t>
<t tx="karstenw.20230615120123.18">def colony(n, x, y, r):
    return Colony(n, x, y, r)
    
</t>
<t tx="karstenw.20230615120123.19">def food(x, y, size):
    return Food(x, y, size)

</t>
<t tx="karstenw.20230615120123.2">class Food:
    
    @others
</t>
<t tx="karstenw.20230615120123.3">def __init__(self, x, y, size):
    self.x = x
    self.y = y
    self.size = size

</t>
<t tx="karstenw.20230615120123.4">class Pheromone:
    
    @others
</t>
<t tx="karstenw.20230615120123.5">def __init__(self, x, y):
    self.x = x
    self.y = y
    self.strength = 1.0
    
</t>
<t tx="karstenw.20230615120123.6">def evaporate(self, d=0.985):
    self.strength *= d
    if self.strength &lt; 0.05: self.strength = 0

</t>
<t tx="karstenw.20230615120123.7">class Ant:

    @others
</t>
<t tx="karstenw.20230615120123.8">def __init__(self, colony, x, y):

    self.colony = colony

    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    
    self.has_food = False
    self.trail = []
    self.wandering = randint(0, 10)

</t>
<t tx="karstenw.20230615120123.9">def near(self, obj, radius=10):
    
    """Checks if something is nearby.
    
    If the object's x and y properties are within 
    the radius of the ant, returns true.
    
    """
    
    dx = abs(self.x-obj.x)
    dy = abs(self.y-obj.y)
    if dx &lt; radius and dy &lt; radius: return True
    else: return False
    
</t>
<t tx="karstenw.20230615120224.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230615120243.1">try:
    ants = ximport("ants")
except:
    ants = ximport("__init__")
    # reload(ants)


size(500,500)
speed(20)

</t>
<t tx="karstenw.20230615120243.2">def setup():    
    
    # Starts a colony with 30 ants in it.
    global colony
    colony = ants.colony(30, WIDTH/2, HEIGHT/2, 100)
    
    # Add some food in the vicinity of the colony.
    for i in range(8):
        x = 50 + random(WIDTH-100)
        y = 50 + random(HEIGHT-100)
        s = random(20,40)
        colony.foodsources.append(ants.food(x,y,s))
    
</t>
<t tx="karstenw.20230615120243.3">def draw():
    
    global colony
    
    fill(0.2)
    rect(0, 0, WIDTH, HEIGHT)
    
    # Draw the hoarded food in the colony.
    fill(0.3)
    s = colony.food
    oval(colony.x-s/2, colony.y-s/2, s, s)
    
    # Draw each foodsource in green.
    # Watch it shrink as the ants eat away its size parameter!
    fill(0.6,0.8,0)
    for f in colony.foodsources:
        # oval(f.x-f.size/2, f.y-f.size/2, f.size, f.size)
        circle(f.x, f.y, f.size/2, f.size/2)
    
    for ant in colony:
        
        stroke(0.8,0.8,0.8,0.5)
        strokewidth(0.5)
        nofill()
        autoclosepath(False)
        
        # Draw the pheromone trail for each ant.
        # Ants leave a trail of scent from the foodsource,
        # enabling other ants to find the food as well!
        if len(ant.trail) &gt; 0:
            beginpath(ant.trail[0].x, ant.trail[0].y)
            for p in ant.trail:
                lineto(p.x, p.y)
            endpath()
        
        # Change ant color when carrying food.
        nostroke()
        fill(0.8,0.8,0.8,0.5)
        if ant.has_food:
            fill(0.6,0.8,0)
        
        # The main ant behaviour:
        # 1) follow an encountered trail,
        # 2) harvest nearby food source,
        # 3) bring food back to colony,
        # 4) wander aimlessly
        ant.forage()
        oval(ant.x, ant.y, 3, 3)
</t>
</tnodes>
</leo_file>
