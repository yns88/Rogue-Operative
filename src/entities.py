'''
Created on Apr 26, 2011

@author: yns88
'''

class Actor:
    nextTurn = 0
    
class Effect(Actor):
    nextTurn = 0
    
class Light(Effect):
    brightness = 0
    radius = 0
    
    def __init__(self,bright,rad):
        self.brightness = bright
        self.radius = rad
        
