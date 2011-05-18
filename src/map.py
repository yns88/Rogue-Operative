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


class map:
	global smap
	def __init__(self,w=len(smap[0]),h=len(smap),format=smap):
		self.width = w
		self.height = h
		
		
		self.tiles = dict()
		self.visible = dict()
		self.explored = dict()

		for i in range(w):
			for j in range(h):
				self.setTile(i,j,(2,0))
				self.visible[(i,j)] = False
				self.explored[(i,j)] = False

		y = 0
		for line in smap:
			x = 0
			for c in line:
				if c == '#':
					self.setTile(x,y,(1,random.randint(0,15)))
				elif c == ' ':
					self.setTile(x,y,(0,random.randint(0,5)))
				else:
					self.setTile(x,y,(-1,0))
				x = x + 1
			y = y + 1
		
	def setTile(self,x,y,tilecode):
		self.tiles[(x,y)] = tilecode
	
	def getTile(self,x,y):
		return self.tiles[(x,y)]

	def isBlocked(self,x,y):
		if self.tiles[(x,y)][0] == 0:
			return False
		else:
			return True
		
	def setVisible(self,x,y,visible):
		self.visible[(x,y)] = visible
	
	def setExplored(self,x,y,vis):
		self.explored[(x,y)] = vis