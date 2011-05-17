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
import copy
import map


'''
Declaration of base variables
'''
curTurn = 0         # the current turn
minTurn = 0         # minimum number of turns to next iteration of game loop

player = player()   # the player character

orc = creatures.Orc(10,10)
bat = creatures.Bat(15,15)
actors = [player,orc,bat]  # player is not in the list of actors, but is always a relevant actor




def initmap(width,height):
    global map
    map = map.map(width,height)
    return map

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
        
        turns.append(turn(map,copy.deepcopy(actors),copy.deepcopy(msgs),curTurn))
        print curTurn
        
        curTurn = minTurn
        
        
        
    
    # if the player can act now, do so
    player.act(curTurn)
    turns.append(turn(map,actors,[msg],curTurn))
    
    return turns
    

class turn:
    def __init__(self, map, actors=[], msgs=[], turn=0):
        self.actors = actors
        self.msgs = msgs
        self.turn = turn
        self.map = map         
        
        
        
            
            
            
