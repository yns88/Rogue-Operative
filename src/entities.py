'''
Created on Apr 26, 2011

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

class Actor:
    nextTurn = 0
    
class Effect(Actor):
    nextTurn = 0
    
class Light(Effect):
    brightness = 0
    radius = 0
    
    def __init__(self,x,y,bright,radius,color=libtcod.orange):
		self.x = x
		self.y = y
		self.brightness = bright
		self.radius = radius
		self.color = color
        
    def getBrightness(self,x,y):
		# Calculate square of the distance to the point
		# must be at least 1
		
		sqr_dist = max(1,((x - self.x)**2 + (y - self.y)**2))
		
		value = 0.04 * self.radius**2 / max(1, sqr_dist)

		
		# value1 = 1.0 / (1.0 + sqr_dist)
		# value2 = value1 - 1.0/(1.0+self.radius**2);
		# value3 = value2 / (1.0 - 1.0/(1.0+self.radius**2));
		
		return max(0,min(1,value))
