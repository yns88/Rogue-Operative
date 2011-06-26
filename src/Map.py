'''
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
import random

smap = ['##############################################',
		'#######################      #################',
		'#####################    #     ###############',
		'######################  ###        ###########',
		'##################      #####             ####',
		'################       ########    ###### ####',
		'###############      #################### ####',
		'################    ######                  ##',
		'########   #######  ######   #     #     #  ##',
		'########   ######      ###                  ##',
		'########                                    ##',
		'####       ######      ###   #     #     #  ##',
		'#### ###   ########## ####                  ##',
		'#### ###   ##########   ###########=##########',
		'#### ##################   #####          #####',
		'#### ###             #### #####          #####',
		'####           #     ####                #####',
		'########       #     #### #####          #####',
		'########       #####      ####################',
		'##############################################',
		]

'''
Map class

fields:
    width:          width of the map
    height:         height of the map
    tiles:          dictionary of position->(tilecode, color variation)
    visible:        dictionary of position->isVisible boolean
    explored:       dictionary of pos->hasBeenExplored boolean
    brightness:     dictionary of pos->brightness float
    colors:         dictionary of pos->background color
    keys:           list of the valid x,y coordinate pairs in this map
    disappeared:    list of the x,y coordinate points that 
                    have recently disappeared from player's pov
'''
class Map:
    global smap
    def __init__(self,format=smap,w=len(smap[0]),h=len(smap)):
        self.width = w
        self.height = h
		
		
        self.tiles = dict()
        self.visible = dict()
        self.explored = dict()
        self.brightness = dict()
        self.colors = dict()
        self.keys = []
        self.disappeared = []
		
        if format is not None:

            for i in range(w):
                for j in range(h):
                    self.setTile(i,j,(2,0))
                    self.explored[(i,j)] = False
                    self.keys.append((i,j))

            y = 0
            for line in smap:
                x = 0
                for c in line:
                    if c == '#':
                        self.setTile(x,y,(1,random.uniform(0.15,0.2)))
                    elif c == ' ':
                        self.setTile(x,y,(0,random.uniform(0.0,0.05)))
                    else:
                        self.setTile(x,y,(-1,0))
                    x = x + 1
                y = y + 1
	
    '''
    setTile:    int, int, int -> void
        sets a tilecode to the given coordinate point
    '''
    def setTile(self,x,y,tilecode):
        self.tiles[(x,y)] = tilecode
	
    '''
    getTile:    int, int -> (int, float)
        reads in a coordinate point and returns the tilecode, color variation
        tuple at that coordinate
        
        returns (0,0) if the coordinate is not valid in this map
    '''
    def getTile(self,x,y):
        if (x,y) in self.keys:
            return self.tiles[(x,y)]
        return (0,0)

    '''
    isBlocked:  int, int -> boolean
        Checks if the tile at the given point blocks vision/movement
    '''
    def isBlocked(self,x,y):
        if self.tiles[(x,y)][0] == 0:
            return False
        else:
            return True
		
    '''
    setVisible: int, int, boolean -> void
        set the visibility of the given point to True, 
        or delete the tile from the list of visible points
    '''
    def setVisible(self,x,y,visible):
        if visible:
            self.visible[(x,y)] = True
        elif (x,y) in self.visible:
            del self.visible[(x,y)]
    
    '''
    getVisible: int, int -> boolean
        return True if the point exists in our visible point list,
        False otherwise
    '''
    def getVisible(self,x,y):
        if (x,y) in self.visible:
            return True
        else:
            return False
	
    '''
    setExplored:    int, int, boolean -> void
        sets the explored value of the given point
    '''
    def setExplored(self,x,y,vis):
        self.explored[(x,y)] = vis
		
    '''
    disappear:  int, int -> void
        adds the given point to the list of recently disappeared points
    '''
    def disappear(self,x,y):
        self.disappeared.append((x,y))
		
    '''
    clearDisappear: void -> void
        resets the recently disappeared list
    '''
    def clearDisappear(self):
        self.disappeared = []
		
    '''
    addBrightness:  int, int, float -> void
        adds a brightness value to the given point
    '''
    def addBrightness(self,x,y,val):
        if (x,y) in self.brightness:
            self.brightness[(x,y)] += val
        else:
            self.brightness[(x,y)] = val

    '''
    getBrightness:  int, int -> float
        returns the brightness value at the given point
    '''
    def getBrightness(self,x,y):
        if (x,y) in self.brightness:
            return self.brightness[(x,y)]
        return 0
    
    '''
    getColor:   int, int -> Color
        returns the background color of the given point
    '''
    def getColor(self,x,y):
        if (x,y) in self.colors:
            return self.colors[(x,y)]
        return libtcod.black
