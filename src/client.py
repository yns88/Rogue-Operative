'''
Created on May 12, 2011

@author: yns88
'''

import console
import engine   # this statement is rather silly
                # obviously once real client/server code is in you won't be importing the engine's source
import libtcodpy as libtcod

lastBlit = -20

if __name__ == "__main__":
    
    #   main game loop
    while not libtcod.console_is_window_closed():
    
        key = libtcod.console_wait_for_keypress(True)
    
        packet = engine.input(key)
        
        for turn in packet:
            
            # screen blits a maximum of once per 10 turns
            # TO DO: find a way to do this without "munching" outlier actions
            if turn.getTurn() - lastBlit > 10:
                lastBlit = turn.getTurn()
                
                # print FPS
                console.showfps()
                
                # update the viewport
                for actor in turn.actors():
                    console.show(actor)
                console.blit(console.viewport)
                
                # update the message port
                for msg in turn.msgs():
                    console.showmessage(msg)
                console.blit(console.message)
                
                # 'disappear' the entities in the viewport to prevent trails
                # this must happen after the last screen flush of the turn
                for actor in turn.actors():
                    console.hide(actor)
                
            else:
                # save any messages that aren't being printed just yet
                for msg in turn.msgs():
                    console.silentmessage(msg)
                    
            