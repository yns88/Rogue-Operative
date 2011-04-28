'''
Created on Apr 25, 2011

@author: yns88
'''

import libtcodpy as libtcod
import keys
import os
import sys
import creatures


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 30
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

curTurn = 0         # the current turn
minTurn = 0         # minimum number of turns to next iteration of game loop

lastBlit = -20


class player(creatures.Creature):
    '''
    The player character
        is a Creature and an Actor
    '''
    
    char = '@'
    speed = 100
    
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2

    def act(self, turn):
        if turn == self.nextTurn:
            key = libtcod.console_wait_for_keypress(True)
            exit = keys.handle_keys(key, self)
                
            self.nextAction()
        
    
            
if __name__ == "__main__":
    player = player()
    orc = creatures.Orc(10,10)
    bat = creatures.Bat(30,30)
    actors = [player,orc,bat]
    
    font = os.path.join('data', 'fonts', 'dejavu10x10_gs_tc.png')
    libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    libtcod.sys_set_fps(LIMIT_FPS)
    
    #   main game loop
    while not libtcod.console_is_window_closed():
        # screen blits a maximum of once per 10 turns
        # TO DO: find a way to do this without "munching" outlier actions
        if curTurn - lastBlit > 10:
            lastBlit = curTurn
            # First, we update the screen
            libtcod.console_set_default_foreground(0, libtcod.white)
            
            # print FPS
            libtcod.console_print_ex(0,SCREEN_WIDTH-1,0, libtcod.BKGND_NONE, libtcod.RIGHT, 'FPS:' + libtcod.sys_get_fps().__str__())
            
            for item in actors:
                libtcod.console_print_ex(0, item.x, item.y, libtcod.BKGND_NONE, libtcod.LEFT, item.char)
            libtcod.console_flush()
            
            # Now, we update the game code
            
            # 'disappear' the entities to prevent trails
            for item in actors:
                libtcod.console_print_ex(0, item.x, item.y, libtcod.BKGND_NONE, libtcod.LEFT, ' ')
    
        minTurn = -1
        
        for item in actors:
            
            if item.nextTurn == curTurn:
                item.act(curTurn)
                
            if minTurn < 0:
                minTurn = item.nextTurn
            elif curTurn < item.nextTurn < minTurn:
                minTurn = item.nextTurn
                    
        
            
        curTurn = minTurn
        
        
        print curTurn
            
            
            