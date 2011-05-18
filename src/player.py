'''
Created on May 12, 2011

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

import creatures
import engine

class player(creatures.Creature):
    '''
    The player character
        is a Creature and an Actor
    '''
    
    char = '@'
    speed = 100
    
    def __init__(self):
        self.x = 9
        self.y = 10

    def act(self, turn):
        if turn == self.nextTurn:            
            self.nextAction()
            engine.fov_recompute()
