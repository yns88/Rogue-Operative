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
import creatures
# from console import *   # import console variable definitions into global
from player import *    # import player definition into global
import copy
import map


class turn:
    def __init__(self, map, actors=[], msgs=[], turn=0, viewchanged=False):
        self.actors = actors
        self.msgs = msgs
        self.turn = turn
        self.map = map
        self.viewchanged = viewchanged
        
        
class fov:
    def __init__(self,width,height,algo=libtcod.FOV_RESTRICTIVE,light_walls=True,radius=10):
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


gamemap = map.map()

fov = fov(gamemap.width,gamemap.height)

for x in range(gamemap.width):
    for y in range(gamemap.height):
        libtcod.map_set_properties(fov.fovmap, x, y, not gamemap.isBlocked(x, y), not gamemap.isBlocked(x, y))
        
def fov_recompute():
    gamemap.clearDisappear()
    libtcod.map_compute_fov(fov.fovmap, player.x, player.y,fov.radius, fov.light_walls, fov.algo)
    for x in range(gamemap.width):
        for y in range(gamemap.height):
            visible = libtcod.map_is_in_fov(fov.fovmap, x, y)
            if visible:
                gamemap.setVisible(x,y,True)
                gamemap.setExplored(x,y,True)
            else:
				if gamemap.getVisible(x,y):
					gamemap.disappear(x,y)
				gamemap.setVisible(x,y,False)

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
                
        visActors = copy.deepcopy(actors)
        for i in range(len(actors)-1,0,-1):
            if not gamemap.getVisible(actors[i].x,actors[i].y):
                visActors.pop(i)
                
        partmap = map.map(None)
        for item in gamemap.visible:
			x = item[0]
			y = item[1]
			if gamemap.getVisible(x,y):
				partmap.setTile(x,y,gamemap.tiles[(x,y)])
				partmap.setVisible(x,y,True)
				partmap.explored[(x,y)] = gamemap.explored[(x,y)]
				partmap.keys.append((x,y))
				partmap.disappear = gamemap.disappear

        turns.append(turn(partmap,visActors,copy.deepcopy(msgs),curTurn))
        print curTurn
        
        curTurn = minTurn
        
        
        
    
    # if the player can act now, do so
    player.act(curTurn)
    
    visActors = copy.deepcopy(actors)
    for i in range(len(actors)-1,0,-1):
        if not gamemap.getVisible(actors[i].x,actors[i].y):
            visActors.pop(i)
            
     
    partmap = map.map(None)
    for item in gamemap.visible:
		x = item[0]
		y = item[1]
		if gamemap.getVisible(x,y):
			partmap.setTile(x,y,gamemap.tiles[(x,y)])
			partmap.setVisible(x,y,True)
			partmap.explored[(x,y)] = gamemap.explored[(x,y)]
			partmap.keys.append((x,y))
			partmap.disappear = gamemap.disappear
    
    turns.append(turn(gamemap,visActors,[msg],curTurn,True))
    
    return turns
    


            
