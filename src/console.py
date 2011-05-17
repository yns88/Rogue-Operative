'''
Created on May 12, 2011

This module attempts to encapsulate much of the really ugly libtcod.console* library calls

@author: yns88
'''

import libtcodpy as libtcod
import os
# import random

class console:
    def __init__(self,width,height,x,y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.con = libtcod.console_new(self.width,self.height)

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

GAME_WIDTH = 55
GAME_HEIGHT = 35

MSG_WIDTH = GAME_WIDTH
MSG_HEIGHT = SCREEN_HEIGHT - GAME_HEIGHT - 1

LIMIT_FPS = 90



font = os.path.join('data', 'fonts', 'dejavu16x16_gs_tc.png')
libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)



libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
libtcod.sys_set_renderer(libtcod.RENDERER_SDL) # stick with SDL for now until other renderers are more stable

viewport = console(GAME_WIDTH,GAME_HEIGHT,0,0)
libtcod.console_set_default_foreground(viewport.con, libtcod.white)

message = console(MSG_WIDTH, MSG_HEIGHT,0,GAME_HEIGHT+1)
libtcod.console_set_default_foreground(message.con, libtcod.white)


# organizing the root console
libtcod.console_set_default_foreground(0, libtcod.white)
for y in range(GAME_HEIGHT):
    libtcod.console_print_ex(0, GAME_WIDTH, y, libtcod.BKGND_NONE, libtcod.LEFT, '|')
for x in range(GAME_WIDTH):
    libtcod.console_print_ex(0, x, GAME_HEIGHT, libtcod.BKGND_NONE, libtcod.LEFT, '_')
libtcod.console_print_ex(0,GAME_WIDTH,GAME_HEIGHT,libtcod.BKGND_NONE, libtcod.LEFT, '/')

# history of messages to the player
# the last element is the most recent message
msghist = [" "," "," "," "," "," "," "," "]

def addmessage(str):
    global msghist
    '''
    silently appends a message to the message history without blitting to the screen
    '''
    if str != None:
        msghist.append(str)
        print(str)


def showmessages(color=libtcod.white):
    global msghist
    '''
    prints the recent message history
    '''
    
    libtcod.console_clear(message.con)
    
    for i in range(1, MSG_HEIGHT):
        
        msgindex = len(msghist) - i
        value = 15*(i-1)
        
        if msgindex > 0:
            libtcod.console_set_default_foreground(message.con, applyval(color,value))
            libtcod.console_print(message.con, 0, MSG_HEIGHT-i, msghist[msgindex])
    

def applyval(color, value):
    newcolor = libtcod.Color(0,0,0)
    if color.r - value > 0:
        newcolor.r = color.r - value
    if color.g - value > 0:
        newcolor.g = color.g - value
    if color.b - value > 0:
        newcolor.b = color.b - value
    
    return newcolor
    
def show(thing):
    libtcod.console_put_char(viewport.con, thing.x, thing.y, thing.char)

def hide(thing, map):
    tile = tiletochar(map.getTile(thing.x,thing.y))
    libtcod.console_put_char_ex(viewport.con, thing.x, thing.y, tile[0],tile[1], tile[2])

def blit(console, ffade=1.0, bfade=1.0):
    libtcod.console_blit(console.con, 0, 0, console.width, console.height, 0, console.x, console.y, ffade, bfade)
    # libtcod.console_flush()
    
def showfps():
    # print FPS
    libtcod.console_print_ex(0,SCREEN_WIDTH-1,SCREEN_HEIGHT-1, libtcod.BKGND_NONE, libtcod.RIGHT, 'FPS:' + libtcod.sys_get_fps().__str__())
    
    
def printmap(map):
	for x in range(0,map.width):
		for y in range(0,map.height):
			tile = tiletochar(map.getTile(x,y))
			libtcod.console_put_char_ex(viewport.con,x,y,tile[0],tile[1],tile[2])
			
def tiletochar(tuple):
	
	
	if tuple[0] == 0:
		return ' ', libtcod.white, applyval(libtcod.desaturated_orange,tuple[1])
	elif tuple[0] == 1:
		return ' ', libtcod.white, applyval(libtcod.dark_sepia,tuple[1])
	else: 
		return 'x', libtcod.pink, libtcod.black
