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
Creature class

fields:
    x:          X coordinate of the object
    y:          Y coordinate of object
    z:          Z coord - which floor level the object is on
    speed:      default speed of creatures is 1 second per base action
    nextAction: lambda function that stores this creature's next action
    char:       character representation of the creature
    effects:    list of Effect objects that are active on this creature

notes:
    Abstract creature data type
    all Creatures are Actors
'''
class Creature(entities.Actor):
    x = None
    y = None
    z = None
    speed = 100
    nextAction = lambda self:0
    char = '.'
    effects = []
    
    '''
    act:    int -> void
        the placeholder act method, this must be overridden
    '''
    def act(self, turn):
        pass
            
    '''
    moveAct:    int, int -> string (or void)
        Standard 2-dimensional move action to a position relative to
        the current position.
        If abs val of relx or rely are greater than 1 then the creature 
        will essentially teleport.
    '''
    def moveAct(self, relx, rely):
        if engine.gamemap.isBlocked(self.x+relx,self.y+rely):
            self.nextAction = lambda: 0
            self.nextTurn += self.speed
            return "You bump your head into the wall"
        
        else:
            self.nextAction = lambda: self.place(self.x+relx, self.y+rely)
            self.nextTurn += self.speed
        
    '''
    wander: void -> void
        move 1 space in a random direction
    '''
    def wander(self):
        self.moveAct(random.randint(-1,1),random.randint(-1,1))
        
    '''
    place:  int, int -> void
        teleport to the given absolute position
    '''
    def place(self, x, y):
        self.x = x
        self.y = y
        
'''
Orc class

parent: Creature

fields:
    no new fields
'''
class Orc(Creature):
    speed = 150
    char = 'o'
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    '''
    act:    int -> void
        check if it's your turn. if it is, then complete the previous
        queued action and then decide to wander in another random 
        direction for your next turn
    '''
    def act(self, turn):
        if turn == self.nextTurn:
            self.nextAction()
            self.wander()
        
'''
Bat class
parent: Creature

fields: no new fields
'''
class Bat(Creature):
    speed = 30
    char = 'b'

    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    '''
    act:    int -> void
        check if it's your turn. if it is, then complete the previous
        queued action and then decide to wander in another random 
        direction for your next turn
    '''
    def act(self, turn):
        if turn == self.nextTurn:
            self.nextAction()
            self.wander()
            
        

