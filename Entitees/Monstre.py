from Entitee import Entitee
from Base import Base
import numpy as np
me = Base(0,0)

#start-of-file

class Monstre(Entitee):

    def __init__(self,id,x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        super().__init__(x,y)
        self.id=id
        self.vx = vx
        self.vy = vy
        self.health = health 
        self.shield_life = shield_life
        self.near_base = near_base
        self.threat_for = threat_for
        self.danger = near_base and (threat_for == 1)
        self.is_controlled = is_controlled
        self.distance = self.distanceTo(me)
        
    def dangerosite(self):
        n = (self.distanceTo(me) - 300)/400 - self.shield_life
        h = self.health/2
        return np.exp(h-n)

    def next_move(self,n=1):
        self.xt,self.yt = self.x,self.y
        for _ in range(n):
            self.xt += self.vx
            self.yt += self.vy
        return Entitee(self.xt,self.yt)

    def __str__(self):
        return "Monstre"

    def shield_off(self):
        return self.shield_life == 0

