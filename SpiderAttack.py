import numpy as np
import sys
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3
heros_id = [[0,3],[1,4],[2,5]]
V = lambda x1,y1,x2,y2: np.array([x2-x1,y2-y1])
N = lambda x1,y1,x2,y2: ( (x2-x1)**2 + (y2-y1)**2 )**0.5
Nv = lambda u : np.dot(u,u)**0.5

xmax,ymax = 17630,9000
xc,yc = xmax//2, ymax//2

xe,ye = xc-base_x + xc,yc-base_y+yc

base_adv_x = base_x + 2*xe
base_adv_y = base_y + 2*ye

adv_x = xc
adv_y = -1

spell = True

class Heros:
    def __init__(self):
        self.heros = {}
        self.spell = True
        self.dispo = ["defenseur","eclaireur","coquin"]
        self.level = 0 #Niveau de dangerosite 
        self.level_inst = 0
        self.temps = 0

    def addHero(self,_id,x, y, shield_life, is_controlled):
        role = self.dispo[int(_id)%3]
        if role == "defenseur":
            self.heros[_id] = Defenseur(x, y, shield_life, is_controlled)
        elif role == "eclaireur":
            self.heros[_id] = Eclaireur(x, y, shield_life, is_controlled)
        elif role == "coquin":
            self.heros[_id] = Coquin(x, y, shield_life, is_controlled)

    def __iter__(self):
        return iter(self.heros.values())
    def __next__(self):
        return next(self)

    def spell_on(self):
        if self.spell:
            self.spell = False
            return True
        else:
            self.spell = True
            return False


    def time_update(self):
        if self.level != self.level_inst:
            self.temps +=1
        else:
            self.temps = 0

    def update_level(self,monstres):
        self.temps+=1
        if (len(monstres.dangerous) > 3 or len(monstres.potentiels) > 6) :
            self.level_inst = 2
        elif len(monstres.potentiels) > 3 :
            self.level_inst = 1
        else:
            self.level_inst = 0
        self.time_update()
        if self.temps > 30:
            self.level = self.level_inst
            self.change_role()
    
    def change_role(self):
        if self.level == 0 :
            self.dispo = ["defenseur","eclaireur","coquin"]
            
        elif self.level == 1:
            self.dispo = ["defenseur","defenseur","coquin"]

        elif self.level == 2:
            self.dispo == ["defenseur","defenseur","eclaireur"]

        for _id in self.heros.keys():
            h = self.heros[_id]
            self.addHero(_id,h.x,h.y,h.shield_life,h.is_controlled)


class Hero(Heros):
    def __init__(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield = shield_life
        self.is_controlled = is_controlled
        self.cible = "-1"
        self.around = []
        self.x0 = x
        self.y0 = y

    def dist_monstre(self,m):
        return N(self.x,self.y,m.x,m.y)

    def update(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield = shield_life
        self.controlled = is_controlled

    def around_him(self,monstres,distance): #Renvoi les menaces les plus proches du hero
        l=[]
        for _id,m in monstres.monstres.items():
            d=N(self.x,self.y,m.x,m.y)
            if  d <= distance and m.threat_for == 1:
                l.append([d,_id])      
        self.around = [ _id for _,_id in sorted(l)]
            
        
    def wait(self):
        print("MOVE",self.x0,self.y0,"WAIT ")
        return True

    def spell(self,monsters,mana):
        pass

    def condition_spell(self):
        return super().spell_on()

class Defenseur(Hero):
    def condition_spell(self,mc,mana,monstres):
        condition_deg1 = mana > 10 and mc.health > 10 and self.dist_monstre(mc) < 1280
        condition_deg2 = len(monstres.dangerous) > 4 or mc.distance < 2000
        return condition_deg1 and condition_deg2 and spell
            
    def attack(self,monstres,mana):
        if self.cible in monstres.dangerous :
            mc = monstres.monstres[self.cible]
            if self.condition_spell(mc,mana,monstres):
                print("SPELL WIND",xc,yc)
                return mana -10
            else:
                print("MOVE",mc.x,mc.y, "Attack target"+self.cible)
                return True
        else :
            if monstres.dangerous:  
                self.cible = monstres.dangerous.pop()
                if monstres.dangerous == []: 
                    monstres.dangerous.append(self.cible)
                mc = monstres.monstres[self.cible]
                if self.condition_spell(mc,mana,monstres):
                    print("SPELL WIND",xc,yc)
                    return 10
                else:
                    print("MOVE",mc.x,mc.y,"Attack danger")
                    return True
            for dist in range(0,2000,200):
                self.around_him(monstres,dist)
                if self.around:
                    self.cible = self.around[0]
                    mc = monstres.monstres[self.cible]
                    print("MOVE",mc.x,mc.y, "Attack around")
                    return True
            return False


class Eclaireur(Hero):
    def __init__(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield = shield_life
        self.controlled = is_controlled
        self.cible = "-1"
        self.around = []
        self.x0 = base_x + (xc - base_x)*3//4
        self.y0 = base_y + (yc - base_y)*3//4
        
    def condition_spell(self,mana,monstres,mc):
        condition_deg1 = mana > 10 and self.dist_monstre(mc) <= 2200
        condition_deg2 = mc.health > 25
        return condition_deg1 and condition_deg2 

    def attack(self,monstres,mana):
        for dist in range(0,1000,100):
            self.around_him(monstres,dist)
            if self.around:
                self.cible = self.around[0]
                mc = monstres.monstres[self.cible]
                if self.condition_spell(mana,monstres,mc):
                    print("SPELL CONTROL",self.cible,xe,ye,"Repousse")
                    return 10
                else:
                    print("MOVE",mc.x,mc.y,"Attack around"+self.cible)
                    return True
        if monstres.potentiels:
            self.cible = monstres.potentiels.pop()
            mc = monstres.monstres[self.cible]
            if mana > 10 and N(self.x,self.y,mc.x,mc.y) <= 2200 and mc.health > 18:
                print("SPELL CONTROL",self.cible,xe,ye,"Repousse")
                return 10
            else:
                print("MOVE",mc.x,mc.y,"Attack potential"+self.cible)
                return True
        return False

class Coquin(Hero):
    def __init__(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield = shield_life
        self.controlled = is_controlled
        self.cible = "-1"
        self.around = []
        self.x0 = xc + (xc - base_x)*3//4
        self.y0 = yc + (yc - base_y)*3//4
        
    
    def around_him(self,monstres,distance): #Renvoi les menaces les plus proches du hero
        l=[]
        for _id,m in monstres.monstres.items():
            d=N(self.x,self.y,m.x,m.y)
            if  d <= distance and m.threat_for == 2:
                l.append([d,_id])      
        self.around = [ _id for _,_id in sorted(l)]
            
    def condition_spell(self,mana,monstres,mc):
        condition_deg1 = mana > 10 and self.dist_monstre(mc) <= 1280
        condition_deg2 = mc.health > 10
        return condition_deg1 and condition_deg2

    def attack(self,monstres,mana):
        for dist in range(0,6000,100):
            self.around_him(monstres,dist)
            if self.around:
                self.cible = self.around[0]
                mc = monstres.monstres[self.cible]
                if self.condition_spell(mana,monstres,mc):
                    print("SPELL WIND",base_adv_x,base_adv_y,"Hihi")
                    return 10
                else:
                    v = V(mc.x,mc.y,xc,yc)
                    v = 900*v/Nv(v)
                    print("MOVE",mc.x+int(v[0]),mc.y+int(v[1]))
                    return True
        return False
    

class Monstres:
    def __init__(self):
        self.monstres = {}
        self.dangerous = []
        self.potentiels = []

    def update_dangerous(self):
        l=[]
        for _id,m in self.monstres.items():
            if m.danger:
                l.append([m.distance,_id])
        self.dangerous = [ _id  for _,_id in sorted(l,reverse=True)]

    def update_potentiels(self):
        l=[]
        for _id,m in self.monstres.items():
            if m.threat_for == 1 and not m.near_base:
                l.append([m.distance,_id])
        self.potentiels = [ _id  for _,_id in sorted(l,reverse=True)]


    def addMonster(self,_id,monstre):
        self.monstres[str(_id)] = monstre

    
    
class Monstre:
    def __init__(self,x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.health = health 
        self.near_base = near_base
        self.threat_for = threat_for
        self.danger = near_base and (threat_for == 1)
        self.distance = N(x,y,base_x,base_y)



heros = Heros()

# game loop
while True:
    monstres = Monstres()
    H=[] #Position des heroes
    health1, mana1 = [int(j) for j in input().split()]
    health2, mana2 = [int(j) for j in input().split()]
    
    mana = mana1
    entity_count = int(input())  # Amount of heros and monsters you can see

    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0 = monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
       
        if _type == 0: 
            monstres.addMonster(_id, Monstre(x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))   

        elif _type == 1:
            if heros.heros.get(str(_id)):
                heros.heros[str(_id)].update(x, y, shield_life, is_controlled)
                #print(f"Hero {str(_id)} 's target", heros[str(_id)].cible,file = sys.stderr )
            else:
                heros.addHero(str(_id),x, y, shield_life, is_controlled)

    monstres.update_dangerous()
    monstres.update_potentiels()
    heros.update_level()
    print(*monstres.dangerous,*monstres.potentiels,sep = "\n",file=sys.stderr)


    ##HEROS ACTION
    #ECLAIREUR
    spell = True
    for hero in heros:
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        m = hero.attack(monstres,mana)
        if type(m) == int: 
            mana -=m
        elif not m:
            hero.wait()
    del monstres