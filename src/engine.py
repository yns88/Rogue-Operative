'''
Created on Apr 25, 2011

@author: yns88
'''

import libtcodpy as libtcod
import keys
# import os
# import sys
import creatures
# from console import *   # import console variable definitions into global
from player import *    # import player definition into global


'''
Declaration of base variables
'''
curTurn = 0         # the current turn
minTurn = 0         # minimum number of turns to next iteration of game loop

lastBlit = -20      # the turn at which the last screen update occurred
                    # initialized to a silly number

player = player()   # the player character


    
def input(key):
    keys.handle_keys(key,player)
    

class turn:
    def __init__(self, actors=[], msgs=[], turn=0):
        self.actors = actors
        self.msgs = msgs
        self.turn = turn

    
            
if __name__ == "__main__":
    player = player()
    orc = creatures.Orc(10,10)
    bat = creatures.Bat(30,30)
    actors = [player,orc,bat]
    

    
    #   main game loop
    while not libtcod.console_is_window_closed():
       
            
                        
        # Now, we update the game code
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
        
        
            
            
            
