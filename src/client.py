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

import libtcodpy as libtcod
import console

'''
    this statement is rather silly
    obviously once real client/server code is in you won't be 
    importing the engine's source
'''
import engine       

# the turn at which the last screen update occurred
# initialized to a silly number
lastBlit = -20      

if __name__ == "__main__":
    
    
    
    #   main game loop
    while not libtcod.console_is_window_closed():
    
        key = libtcod.console_wait_for_keypress(True)
    
        packet = engine.play(key)
        
        for turn in packet:
            
            console.printmap(turn.map)
            
            # print FPS
            console.showfps()
            
            # screen blits a maximum of once per 10 turns
            # TO DO: find a way to do this without "munching" outlier actions
            if turn.turn - lastBlit > 0:
                lastBlit = turn.turn

                # update the viewport
                for actor in turn.actors:
                    console.show(actor)
                console.blit(console.viewport)
                
                
                # update the message port
                for msg in turn.msgs:
                    console.addmessage(msg)

                console.showmessages(libtcod.light_orange)
                    
                console.blit(console.message)
                
                libtcod.console_flush()
                
                # 'disappear' the entities in the viewport to prevent trails
                # this must happen after the last screen flush of the turn
                for actor in turn.actors:
                    console.hide(actor,turn.map)
                    
                
            else:
                # save any messages that aren't being printed just yet
                for msg in turn.msgs:
                    console.addmessage(msg)
                    
                # print messages anyway
                console.showmessages(libtcod.light_orange)
                console.blit(console.message)
                libtcod.console_flush()
                    
            