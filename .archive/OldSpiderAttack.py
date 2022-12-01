
## OLD VERSION
#%%


import sys
import math
import numpy as np
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

V = lambda x1,y1,x2,y2: np.array([x2-x1,y2-y1])
N = lambda x1,y1,x2,y2: ( (x2-x1)**2 + (y2-y1)**2 )**0.5
Nv = lambda u : np.dot(u,u)**0.5


def vers_base(x,y,vx,vy):
    return np.dot(V(x,y,base_x,base_y),V(0,0,vx,vy)) > 0

def around(xm,ym,xh,yh):
    M = V(xm,ym,base_x,base_y)
    H = V(xh,yh,base_x,base_y)
    return (np.dot(M,H) > 0)


X=17630
Y=9000 
D=(X**2 + Y**2)**0.5

u_init = V(base_x,base_y,X/2,Y/2)
x0,y0 =-1,-1

def move_monster(xm,ym,vx,vy):
    v = V(vx,vy,0,0)
    #vu = v / Nv(v) if Nv(v) else np.array([0,0])
    p = V(0,0,xm,ym) 
    print( "MOVE",int( p[0] ),int( p[1] ) ) 

cibles=[None,None,None]
pos=[[0,0],[0,0],[0,0]]

# game loop
while True:
    H=[] #Position des heroes
    for i in range(2):
        # health: Each player's base health
        # mana: Ignore in the first league; Spend ten mana to cast a spell
        health, mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see
    monster_danger = [[],[]] #[ [Monstres qui cible la base], [Monstres qui se dirige vers la base]]
    monsters=[]

    monsters_key = []
    monsters_val = []

    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        
        if _type == 0: #Monstre
            
            monsters_key.append(_id)
            monsters_val.append([x,y,vx,vy])

            dist = N(base_x,base_y,x,y)
            monsters.append([x,y,vx,vy])
            if near_base and dist < 6000:
                monster_danger[0].append([dist,x,y,vx,vy])
            elif threat_for == 1:
                monster_danger[1].append([dist,x,y,vx,vy])

        elif _type == 1: #Hero
            if x0 == -1 and y0 == -1:
                x0,y0=x,y   
            pos[_id] = [x,y]


    monster_danger[0].sort()
    monster_danger[1].sort()

        
    for i in range(heroes_per_player):
        test=True
        if cibles[i] in monsters_key:
            x,y,vx,vy = monsters_val[monsters_key.index(cibles[i])]
            move_monster(x,y,vx,vy)
            test=False
            
        else:
            if len(monster_danger[0]):
                x,y,vx,vy = monster_danger[0].pop()[1:]
                cible = monsters_key[monsters_val.index([x,y,vx,vy])]
                if N(x,y,pos[i][0],pos[i][1]) <= 2200 and N(x,y,base_x,base_y) <600 and mana > 10:
                    print("SPELL CONTROL",cible,int(X/2),int(Y/2))
                    test=False
                    mana-=10
                else:
                    cibles[i]=cible
                    move_monster(x,y,vx,vy)
                    test=False
            elif len(monster_danger[1]):
                x,y,vx,vy = monster_danger[1].pop()[1:]
                cibles[i] = monsters_key[monsters_val.index([x,y,vx,vy])]
                move_monster(x,y,vx,vy)
                test=False
            
            else:
                print("MOVE",x0,y0)
                cibles[i] = None
                test=False
        if test:
            print("WAIT")

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)


        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        



