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
	def __init__(self,w,h,format=smap):
		self.width = w
		self.height = h
		
		
		self.tiles = dict()


		for i in range(w):
			for j in range(h):
				self.setTile(i,j,(2,0))

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