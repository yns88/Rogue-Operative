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
        if engine.gamemap.isBlocked(self.x+relx,self.y+rely):
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