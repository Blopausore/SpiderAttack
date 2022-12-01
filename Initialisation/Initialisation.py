#start-of-file
#%%
import numpy as np
import sys
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3
heros_id = [[0,3],[1,4],[2,5]]

id_joueur = 1 if (base_x,base_y) == (0,0) else 2

V = lambda x1,y1,x2,y2: np.array([x2-x1,y2-y1])
N = lambda x1,y1,x2,y2: ( (x2-x1)**2 + (y2-y1)**2 )**0.5
Nv = lambda u : np.dot(u,u)**0.5

global monstres
global heros


identitee = lambda e : True

xmax,ymax = 17630,9000
xc,yc = xmax//2, ymax//2

base_adv_x = (xc - base_x)*2 + base_x
base_adv_y = (yc - base_y)*2 + base_y

mana = 0

heros = Heros()
monstres = Monstres()
adversaires = Adversaires()