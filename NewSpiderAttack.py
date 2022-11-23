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


#### CLASS HEROS #################################################################################
#%%
class Heros:
    def __init__(self):
        self.heros = {}
        self.spell = True
        self.dispo = ["defenseur","chasseur","chasseur"]
        self.level = 1 #Niveau de dangerosite 
        self.level_inst = 1
        self.temps = 0
        self.phase = 0
    
    def initEnd(self):
        self.init_pos_chasseur()

    def __iter__(self):
        return iter(self.heros.values())

    def __next__(self):
        return next(self)

    def initHero(self,_id,x, y, shield_life, is_controlled):
        role = self.dispo[int(_id)%3]
        if role == "defenseur":
            self.heros[_id] = Defenseur(x, y, shield_life, is_controlled)
            print("Changement fait.",file=sys.stderr)
        elif role == "eclaireur":
            self.heros[_id] = Eclaireur(x, y, shield_life, is_controlled)
            print("Changement fait.",file=sys.stderr)
        elif role == "coquin":
            self.heros[_id] = Coquin(x, y, shield_life, is_controlled)
            print("Changement fait.",file=sys.stderr)
        elif role == "chasseur":
            self.heros[_id] = Chasseur(x, y, shield_life, is_controlled)
            print("Changement fait.",file=sys.stderr)
        else:
            print("Erreur role inconnu",_id,file=sys.stderr)


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
        if monstres.maxhealth >= 14 and self.phase == 0:
            self.phase = 1
            self.level_inst = 1
            self.level = self.level_inst
            self.change_role()
        elif monstres.maxhealth >= 20 and self.phase == 1:
            self.phase = 2
            self.level_inst = 2
            self.level = self.level_inst
            self.change_role()

        elif len(monstres.allies) > 2:
            self.level_inst = -1
        else:
            self.level_inst = self.level
        self.time_update()

        if self.temps > 30:
            self.temps = 0
            self.level = self.level_inst
            self.change_role()
    
    def change_role(self):
        if self.level == -1:
            self.dispo = ["defenseur","defenseur","coquin"]

        elif self.level == 0 :
            self.dispo = ["defenseur","chasseur","chasseur"]

        elif self.level == 1 :
            self.dispo = ["defenseur","defenseur","chasseur"]

        elif self.level == 2:
            self.dispo = ["defenseur","defenseur","eclaireur"]


        for _id in self.heros.keys():
            h = self.heros[_id]
            self.initHero(_id,h.x,h.y,h.shield_life,h.is_controlled)

    def init_pos_chasseur(self):
        nb = self.dispo.count("chasseur")
        d = ymax//(nb+1)
        for h in self:
            if h.role == "chasseur":
                h.y0 = nb*d
                nb-=1
#### CLASS ENTITEE / Adversaire ##############################################################################

class Entitee:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def update(self,x,y):
        self.x = x
        self.y = y

    def distanceTo(self,other):
        return N(self.x,self.y,other.x,other.y)

class Adversaires:
    def __init__(self):
        self.adversaires = {}

    def initAdversaire(self,_id,x, y, shield_life, is_controlled):
        self.adversaires[_id] = Adversaire(x,y,shield_life,is_controlled)
        
class Adversaire(Entitee):
    def __init__(self,x,y, shield_life, is_controlled):
        super().__init__(x,y)
        self.shield_lif = shield_life
        self.is_controlled = is_controlled


#### CLASS HERO #################################################################################
#%%
class Hero(Heros,Entitee):
    def __init__(self,x,y,shield_life,is_controlled):
        super().__init__()
        self.x = x
        self.y = y
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.cible = "-1"
        self.around = []
        self.x0 = x
        self.y0 = y
        self.init_spe()

    def init_spe(self):
        pass

    def dist_monstre(self,m):
        return N(self.x,self.y,m.x,m.y)

    def update(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield_life= shield_life
        self.is_controlled = is_controlled

    def update_around(self,monstres,distance,reverse = False):
        self.around = []
        for _id,m in monstres:
            d=self.dist_monstre(m)
            if  d <= distance:
                self.around.append([d,_id])      
        self.around = [ _id for _,_id in sorted(self.around,reverse=reverse)]
            
        
    def wait(self):
        print("MOVE",self.x0,self.y0,"WAIT ")
        return True

    def condition_spell(self):
        return super().spell_on()

class Defenseur(Hero):
    def init_spe(self):
        self.role = "defenseur" 


    def attack(self,monstres,mana):
        pass

class Eclaireur(Hero):
    def init_spe(self):
        self.role = "eclaireur"
    
    def attack(self,monstres,mana):
        pass

class Coquin(Hero):
    def init_spe(self):
        self.role="coquin"

    def attack(self,monstres,mana):
        pass

class Chasseur(Hero):
    def init_spe(self):
        self.role="chasseur"
    
    def attack(self,monstres,mana):
        pass

#### CLASS COMPORTEMENT #################################################################################
#%%
class Comportement(Hero):
    def __init__(self):
        self.cible = str()


    def attaque(self,mc): #mc : monstre cible
        print(f"MOVE {mc.x} {mc.y}")
        return True

    def attaque_cible(self,monstres):
        if self.cibles in monstres.keys():
            return self.attaque(monstres[self.cible])

    def wind(self,mc):
        if super().distanceTo(mc) <= 1280 and super().getMana():


    def getAround(self,monstres,distance,reverse=False):
        super().update_around(monstres,distance,reverse=reverse)
        return super().around()

class Defense(Comportement):


    def defense_exterieur(self):
        pass

    def defense_interieur(self):
        pass


class Chasse(Comportement):

    def chasse(self,monstres):
        
        if self.attaque_cible(monstres):
            return True
    
        around = super().getAround(monstres,5000,reverse=True)
        if around:
            self.cible = around.pop()
            return self.attaque(monstres[self.cible])
        return False


class Attaque(Comportement):
    pass


#### CLASS MONSTRES #################################################################################
#%%
class Monstres:
    def __init__(self):
        self.monstres = {}
        self.dangerous = []
        self.potentiels = []
        self.allies = []
        self.maxhealth = 0

    def __iter__(self):
        return iter(self.monstres.items())

    def __next__(self):
        return next(self)

    def keys(self):
        return self.monstres.keys()

    def addMonster(self,_id,monstre):
        self.maxhealth = max(self.maxhealth,monstre.health)
        self.monstres[str(_id)] = monstre

    def update_dangerous(self):
        l=[]
        for _id,m in self:
            if m.danger:
                l.append([m.distance,_id])
        self.dangerous = [ _id  for _,_id in sorted(l,reverse=True)]

    def update_potentiels(self):
        l=[]
        for _id,m in self:
            if m.threat_for == 1 and not m.near_base:
                l.append([m.distance,_id])
        self.potentiels = [ _id  for _,_id in sorted(l,reverse=True)]

    def update_allies(self):
        self.allies=[]
        for _id,m in self:
            if m.threat_for == 2 and m.near_base:
                self.allies.append([_id])




    
    
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
        self.is_controlled = is_controlled





#### LOOP #################################################################################
#%%
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
                heros.initHero(str(_id),x, y, shield_life, is_controlled)
                heros.initEnd()

    monstres.update_dangerous()
    monstres.update_potentiels()
    heros.update_level(monstres)

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