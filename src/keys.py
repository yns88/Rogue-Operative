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
import sys
import console

# movement keys
UP = [ord('k'),libtcod.KEY_KP8]
DOWN = [ord('j'),libtcod.KEY_KP2]
LEFT = [ord('h'),libtcod.KEY_KP4]
RIGHT = [ord('l'),libtcod.KEY_KP6]
UPLEFT = [ord('y'),libtcod.KEY_KP7]
UPRIGHT = [ord('u'),libtcod.KEY_KP9]
DOWNLEFT = [ord('b'),libtcod.KEY_KP1]
DOWNRIGHT = [ord('n'),libtcod.KEY_KP3]

ESCAPE = [libtcod.KEY_ESCAPE]


def handle_keys(key, player):
    
    # check if a given key has been pressed
    def check_key_pressed(keyname):
        for item in keyname:
            if key.vk == item or key.c == item: 
                return True
        return False
    
    
    # movement keys
    
    # up
    if check_key_pressed(UP):
        return player.moveAct(0,-1)
    
    # down
    elif check_key_pressed(DOWN):
        return player.moveAct(0,1)
    
    # left
    elif check_key_pressed(LEFT):
        return player.moveAct(-1,0)
    
    # right
    elif check_key_pressed(RIGHT):
        return player.moveAct(1,0)
    
    # upleft
    elif check_key_pressed(UPLEFT):
        return player.moveAct(-1,-1)
    
    # upright
    elif check_key_pressed(UPRIGHT):
        return player.moveAct(1,-1)
        
    # downleft
    elif check_key_pressed(DOWNLEFT):
        return player.moveAct(-1,1)
        
    # downright
    elif check_key_pressed(DOWNRIGHT):
        return player.moveAct(1,1)

    elif check_key_pressed(ESCAPE):
        sys.exit(0)
    
    else:
        player.nextAction = lambda: 0
        
        # stupid system has no easy way of figuring out what the key pressed was if it's not a printable char
        msg = "Unknown command"
        
        if key.vk == libtcod.KEY_CHAR:
            msg += ": {char}".format(char=chr(key.c))
        return msg
    