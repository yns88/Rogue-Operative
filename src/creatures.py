'''
Created on Apr 26, 2011

@author: yns88
'''

import libtcodpy as libtcod
import entities
import random
import engine

'''
    Abstract creature data type
        all Creatures are Actors
'''
class Creature(entities.Actor):
    x = None            # X coordinate of object
    y = None            # Y coordinate of object
    z = None            # Z coord - which floor level the object is on
    speed = 100         # default speed of creatures is 1 second per base action
    nextAction = lambda self:0   # lambda function that stores this creature's next action
    char = '.'          # character representation of the creature
    effects = []        # list of Effect objects that are active on this creature
    
    def act(self, turn):
        self.nextAction()
            
    '''
    Standard 2-dimensional move action
    If abs val of relx or rely are greater than 1 then the creature will essentially teleport
    '''
    def moveAct(self, relx, rely):
        if engine.map.isBlocked(self.x+relx,self.y+rely):
            self.nextAction = lambda: 0
            self.nextTurn += self.speed
            return "You bump your head into the wall"
        
        else:
            self.nextAction = lambda: self.place(self.x+relx, self.y+rely)
            self.nextTurn += self.speed
        
    def wander(self):
        self.moveAct(random.randint(-1,1),random.randint(-1,1))
        
    def place(self, x, y):
        self.x = x
        self.y = y
        

class Orc(Creature):
    speed = 150
    char = 'o'
    
    def act(self, turn):
        if turn == self.nextTurn:
            self.nextAction()
            self.wander()
            
        
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class Bat(Creature):
    speed = 30
    char = 'b'
    
    def act(self, turn):
        if turn == self.nextTurn:
            self.nextAction()
            self.wander()
            
        
    def __init__(self,x,y):
        self.x = x
        self.y = y