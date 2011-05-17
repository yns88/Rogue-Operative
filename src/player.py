'''
Created on May 12, 2011

@author: yns88
'''

import creatures

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
