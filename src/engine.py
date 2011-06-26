'''
Created on Apr 25, 2011

    Rogue Operative - A Roguelike Espionage Game
    Copyright (C) 2011  yns88 <yns088@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import libtcodpy as libtcod
import keys
# import os
# import sys
import entities
import creatures
# from console import *   # import console variable definitions into global
from player import *    # import player definition into global
import copy
import Map


"""
Turn structure:

fields:
    map:        the game map (according to player's view) on this turn
    turn:       the turn number, which shows us exactly when the turn took place
    actors:     the list of entities which act on this turn
                    defaults to empty list
    msgs:       the list of messages sent to the player on this turn
                    defaults to empty list
    viewchanged:whether or not the player's view has changed on this turn
                    defaults to false
"""
class turn:
    def __init__(self, _map, turn=0, actors=[], msgs=[], viewchanged=False):
        self.actors = actors
        self.msgs = msgs
        self.turn = turn
        self.map = _map
        self.viewchanged = viewchanged
        
"""
Field of View structure

fields:
    algo:           the algorithm used to determine what's in the field of view 
                        defaults to libtcod.FOV_RESTRICTIVE
    light_walls:    whether or not to light up walls in the map
                        defaults to True
    radius:         the radius of vision
                        defaults to 15 tiles
                        
methods:
    setRadius:      number -> void
                    changes the radius in this field of view map
"""        
class fov:
    def __init__(self,width,height,algo=libtcod.FOV_RESTRICTIVE,light_walls=True,radius=15):
            self.algo = algo
            self.light_walls = light_walls
            self.radius = radius
            self.fovmap = libtcod.map_new(width, height)
      
    def setRadius(self,r):
		self.radius = radius



'''
Declaration of base variables
'''
curTurn = 0         # the current turn
minTurn = 0         # minimum number of turns to next iteration of game loop

player = player()   # the player character

orc = creatures.Orc(10,10)
bat = creatures.Bat(15,15)
bat2 = creatures.Bat(8,8)
actors = [player,orc,bat,bat2]  # player is not in the list of actors, but is always a relevant actor
lights = []

testlight = entities.Light(37,7,50,10)
lights.append(testlight)
testlight2 = entities.Light(9,10,1,10)
lights.append(testlight2)

gamemap = Map.Map()

myfov = fov(gamemap.width,gamemap.height)

for x in range(gamemap.width):
	for y in range(gamemap.height):
		libtcod.map_set_properties(myfov.fovmap, x, y, not gamemap.isBlocked(x, y), not gamemap.isBlocked(x, y))

'''
fov_recompute:  void -> void
    recompute the FOV for the player, and adjusts the game map accordingly
'''
def fov_recompute():
    gamemap.clearDisappear()
    libtcod.map_compute_fov(myfov.fovmap, player.x, player.y,myfov.radius, myfov.light_walls, myfov.algo)
    for x in range(gamemap.width):
        for y in range(gamemap.height):
            visible = libtcod.map_is_in_fov(myfov.fovmap, x, y)
            if visible:
                gamemap.setVisible(x,y,True)
                gamemap.setExplored(x,y,True)
            else:
				if gamemap.getVisible(x,y):
					gamemap.disappear(x,y)
				gamemap.setVisible(x,y,False)
				
'''
lights_recompute:   void -> void
    recompute the FOV for the lights, and adjust the game map accordingly
'''
def lights_recompute():
	gamemap.brightness = dict()
	for light in lights:
		libtcod.map_compute_fov(myfov.fovmap, light.x, light.y, light.radius, False, myfov.algo)
		for x in range(light.x-light.radius,light.x+light.radius):
			for y in range(light.y-light.radius,light.y+light.radius):
				if libtcod.map_is_in_fov(myfov.fovmap,x,y):
					gamemap.addBrightness(x,y,light.getBrightness(x,y))
					gamemap.colors[(x,y)] = light.color # change this later
				
lights_recompute()
			
'''
getVisibleMap():    void -> Map.Map
    creates a partial map based on information the player knows about
    the current situation, and then returns it

'''
def getVisibleMap():
    partmap = Map.Map(None)
    for x,y in gamemap.visible:
        if gamemap.getVisible(x,y):
            partmap.setTile(x,y,gamemap.tiles[(x,y)])
            partmap.setVisible(x,y,True)
            partmap.explored[(x,y)] = gamemap.explored[(x,y)]
            partmap.keys.append((x,y))
            partmap.disappear = gamemap.disappear
            partmap.brightness[(x,y)] = gamemap.getBrightness(x,y)
            partmap.colors = gamemap.colors
    return partmap

'''
pruneActors:    void -> list of actors
    
    creates a copy of the game's list of actors and then removes those
    that are not visible to the player
'''
def getVisActors():
    visActors = copy.deepcopy(actors)
    for i in range(len(actors)-1,0,-1):
        if not gamemap.getVisible(actors[i].x,actors[i].y):
            visActors.pop(i)
    return visActors

'''
play:   key ID -> list of Turns

    This is the loop in which the game logic is calculated. A packet of
    turns which each store information about what happened in that turn
    is generated and then returned to the client

'''
def play(key):
    global curTurn,minTurn,player,actors
    
    turns = []
    
    
    # evaluate the provided input
    # this will set the player's next action
    # the return value is a string message to the player
    msg = keys.handle_keys(key,player)
    
    
    # now we loop through all the turns between player inputs
    while curTurn < player.nextTurn:
        msgs = []
        
        # the minimum value of the next turn is when the player will next act
        minTurn = player.nextTurn

        # now we tell all the other actors to act
        for item in actors:
            
            if item.nextTurn == curTurn:
                item.act(curTurn)

            if curTurn < item.nextTurn < minTurn:
                minTurn = item.nextTurn
                
        visActors = getVisActors()
        partmap = getVisibleMap()
        
        # generate a turn with this turn's information and then append it
        turns.append(turn(partmap,curTurn,visActors,copy.deepcopy(msgs)))
        
        # update the game to the next turn in which something will happen
        curTurn = minTurn
        
        
        
    
    # if the player can act now, do so
    player.act(curTurn)
    
    # create a copy of our actors list and prune out those that are not visible
    visActors = getVisActors()
    
    partmap = getVisibleMap()
    
    # append the final turn when the player's action is complete
    turns.append(turn(gamemap,curTurn,visActors,[msg],True))
    
    return turns
    


            
