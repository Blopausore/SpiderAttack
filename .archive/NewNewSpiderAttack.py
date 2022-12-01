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



#### CLASS ENTITEE / Adversaire ##############################################################################

class Entitee:
    def __init__(self,id,x,y):
        self.x = x
        self.y = y
        self.id = id

    def update(self,x,y):
        self.x = x
        self.y = y

    def distanceTo(self,other):
        return N(self.x,self.y,other.x,other.y)

    def vectTo(self,other):
        return (other.x - self.x, other.y - self.y)


class Base(Entitee):
    def __init__(self,x,y):
        super().__init__("BASE",x,y)
        self.counter_near = 0
        self.counter_potentiel = 0
        self.evolution = 0
        self.dangerosite0 = 0
        self.dangerosite1 = 0

    def dangerosite(self):
        return self.counter_near * 3 + self.counter_potentiel

    def update_near(self):
        filtre = lambda m : m.danger
        self.counter_near = len(list(filter(filtre, monstres.closests)))

    def update_potentiel(self):
        filtre = lambda m : m.threat_for == 1 and not m.near_base
        self.counter_near = len(list(filter(filtre, monstres.closests)))

    def update(self):
        self.update_near()
        self.update_potentiel()
        self.dangerosite0 = self.dangerosite1
        self.dangerosite1 = self.dangerosite()
        self.evolution = self.dangerosite1 - self.dangerosite0

class Centre(Entitee):
    def __init__(self,x,y):
        self.x=x
        self.y=y

centre = Centre(xc,yc)
me = Base(base_x,base_y)
uo = Base(base_adv_x,base_adv_y)

#### CLASS Adversaire ##############################################################################
class Adversaires:
    def __init__(self):
        self.adversaires = {}

    def __iter__(self):
        return iter(self.adversaires.values())

    def __next__(self):
        return next(self)

    def initAdversaire(self,_id,x, y, shield_life, is_controlled):
        self.adversaires[_id] = Adversaire(_id, x, y, shield_life, is_controlled)
        


class Adversaire(Entitee):
    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(id, x, y)
        self.shield_life = shield_life
        self.is_controlled = is_controlled

    def update(self, x, y, shield_life, is_controlled):
        self.x = x
        self.y = y
        self.shield_life = shield_life
        self.is_controlled = is_controlled

    def shield_off(self):
        return self.shield_life == 0

adversaires = Adversaires()
#### CLASS MONSTRES #################################################################################
#%%

class Monstres:
    def __init__(self):
        self.monstres = {}
        self.allies = []
        self.maxhealth = 0
        self.closests = []


    def __iter__(self):
        return iter(self.monstres.values())

    def __next__(self):
        return next(self)

    def keys(self):
        return self.monstres.keys()

    def addMonster(self,_id,monstre):
        self.maxhealth = max(self.maxhealth,monstre.health)
        self.monstres[str(_id)] = monstre

    def update_closest(self):
        self.closests = sorted(self,key = lambda m : m.distance)

    def update_allies(self):
        filtre = lambda m : m.threat_for == 2 and m.near_base
        self.allies=list(filter(filtre, self.monstres.values()))

    def update(self):
        self.update_closest()
        self.update_allies()

    def is_alive(self,monstre):
        return (monstre.is_alive() and monstre.id in self.keys())


    
class Monstre(Entitee):

    def __init__(self,id,x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        super().__init__(id,x,y)
        self.vx = vx
        self.vy = vy
        self.health = health 
        self.shield_life = shield_life
        self.near_base = near_base
        self.threat_for = threat_for
        self.danger = near_base and (threat_for == 1)
        self.is_controlled = is_controlled
        self.distance = self.distanceTo(me)

    def is_alive(self):
        return self.id != -1

    def shield_off(self):
        return self.shield_life == 0

class MonstreNull(Monstre):
    def __init__(self):
        pass

    def is_alive(self):
        return False


#### CLASS HERO #################################################################################
#%%
class Hero(Entitee):
    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(id, x, y)
        self.id = id
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.cible = MonstreNull()
        self.around = [MonstreNull()]
        self.x0 = x
        self.y0 = y
        self.comportements = []
        self.reactions = [] #Pile de comportement employe qu'une fois

    def __iter__(self):
        return iter([self])

    def __next__(self):
        return next(self)

    def update(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield_life= shield_life
        self.is_controlled = is_controlled

    def update_around(self,reverse = False):
        self.around = list(sorted(monstres,key = lambda m : self.distanceTo(m)))        

    def shield_off(self):
        return self.shield_life == 0

    def play(self):
        print(self.id,file=sys.stderr)
        print("\t",*self.comportements,file=sys.stderr)
        print("\t",*self.reactions, file=sys.stderr)
        for i,reaction in enumerate(self.reactions):
            action = reaction(self).action()
            if action:
                del self.reactions[i]
                return action

        for comportement in self.comportements:
            action = comportement(self).action()
            if action:
                return action

        print("Erreur : aucun comportements acceptes",file = sys.stderr)
        print(*[str(comportement) for comportement in self.comportements],file = sys.stderr)

#### CLASS COMPORTEMENT #################################################################################
#%%

class Comportement:
    def __init__(self,hero):
        self.cible = None
        self.hero = hero

    def __str__(self):
        return "Comportement"
    
    def __iter__(self):
        return iter([self])

    def __next__(self):
        return next(self)

    def getCible(self):
        return self.hero.cible

    def setCible(self,monstre):
        self.hero.cible = monstre

    def attaque(self, mc, cibler=False): #mc : monstre cible
        if cibler : self.hero.cible = mc
        print(f"MOVE {mc.x} {mc.y}")
        return True

    def actionClosest(self,action=attaque,filtre=identitee,**actionArgs):
        for monstre in filter(filtre, self.hero.around):
            return action(monstre,actionArgs)
        return False



    #SPELL
    def wind(self,mc,x,y):
        if self.hero.distanceTo(mc) <= 1280 and mana >= 10 and mc.shield_off():
            print(f"SPELL WIND {x} {y}")
            return 10
        return False

    def shield(self,e):
        if self.hero.distanceTo(e) <= 2200 and mana >= 10:
            print(f"SPELL SHIELD {e.id}")
            return 10
        return False

    def control(self,e,x,y):
        if self.hero.distanceTo(e) <= 2200 and mana >= 10 and e.shield_off() and not e.is_controlled:
            print(f"SPELL CONTROL {e.id} {x} {y}")
            return 10
        return False

## I BASIQUE
class Wait(Comportement):
    def action(self):
        print("MOVE",self.hero.x0,self.hero.y0,"WAIT ")
        return True

    def __str__(self):
        return "WAIT"

class AttaqueCible(Comportement):
    def __init__(self,hero,filtre = identitee):
        super().__init__(hero)
        self.filtre = filtre
    
    def __str__(self):
        return "AttaqueCible"

    def action(self):
        cible = self.getCible()
        if monstres.is_alive(cible) and self.filtre(cible):
            return self.attaque(cible)
        return False

        
## II

## III Defense
### III.1 Defense basique
class DefenseWind(Comportement):
    def __init__(self,hero):
        super().__init__(hero)
        self.distance = 2000

    def __str__(self):
        return "DefenseWind"

    def action(self):
        filtre = lambda m : m.shield_off() and m.distance < self.distance and m.health > 5 and m.danger
        for monstre in filter(filtre,monstres.closests):
            return self.wind(monstre,xc,yc) 
        return False

class DefenseInterne(Comportement):
    def __str__(self):
        return "DefenseInterieur"
    def action(self):
        filtre = lambda m : m.danger == 1 
        for monstre in filter(filtre,monstres.closests):
            if not heros.is_target(monstre):
                self.setCible(monstre)
                return self.attaque(monstre)
        for monstre in filter(filtre,monstres.closests):
            self.setCible(monstre)
            return self.attaque(monstre)
        return False

class DefenseInterneOpti(Comportement):
    def __str__(self):
        return "DefenseInterneOpti"
    def __init__(self,hero):
        super().__init__(hero)
        self.vhx,self.vhy = hero.vectTo(me)

    def dot(self,monstre):
        vmx,vmy = monstre.vectTo(self.hero)
        return self.vhx * vmx + self.vhy * vmy

    def action(self):
        filtre = lambda m : m.danger
        for monstre in filter(filtre,sorted(monstres.closests,key = self.dot)):
            if not heros.is_target(monstres):
                self.setCible(monstre)
                return self.attaque(monstre)
        for monstre in filter(filtre,sorted(monstres.closests,key = self.dot)):
            self.setCible(monstre)
            return self.attaque(monstre)
        return False

### III.2 Defense externe
class DefenseExterne(Comportement):
    def __str__(self):
        return "DefenseExterieur"

    def action(self):
        filtre = lambda m : m.threat_for == 1 and not m.near_base and m.distance < 12000
        for monstre in filter(filtre, self.hero.around):
            if not heros.is_target(monstre):
                self.setCible(monstre)
                return self.attaque(monstre)

        for monstre in filter(filtre, self.hero.around):
            self.setCible(monstre)
            return self.attaque(monstre)
        return False

class DefenseRedirection(Comportement):
    def __str__(self):
        return "DefenseRedirection"

    def action(self):
        filtre = lambda m : m.health > 20 and m.shield_off()
        return self.actionClosest(self.control,filtre,x=uo.x,y=uo.y)


### III.3 Defense adversaire

class DefenseAdvRedirection(Comportement):
    def __str__(self):
        return "DefenseAdvRedirection"

    def action(self):
        key_ = lambda adversaire : adversaire.distanceTo(self.hero)
        for adversaire in sorted(adversaires,key=key_):
            if self.control(adversaire,uo.x,uo.y):
                return 10
        return False

class DefenseHeroShield(Comportement):
    def __str__(self):
        return "DefenseAdvShield"

    def action(self):
        filtre = lambda hero : hero.is_controlled 
        key_ = lambda hero : hero.distanceTo(self.hero)
        for hero in filter(filtre,sorted(heros,key=key_,reverse=True)):
            if self.shield(hero):
                return 10
        return False

class DefenseIntensive(Comportement):
    def __str__(self):
        return "DefenseIntensive"

    def action(self):
        filtre = lambda monstre : not monstre.shield_off() and monstre.health > 5 and monstre.distanceTo(me)
        return self.actionClosest(self.attaque,filtre)



## IV Attaque
### IV.1 Attaque externe


##### COMBO ######################################################################

class Combo:
    def __init__(self):
        pass

    def __iter__(self):
        return iter(self)

    def __next__(self):
        return next(self)


#### CLASS HEROS #################################################################################
#%%
class Heros:
    def __init__(self):
        self.heros = {}
        
    def __iter__(self):
        return iter(self.heros.values())

    def __next__(self):
        return next(self)

    
    def update_positionnement(self, heros ,distance):
        if distance < 10000:
            if distance < 5000 and len(list(filter(lambda m : m.danger,monstres))) == 0 :
                distance = 6000
            u = 1 if id_joueur == 1 else -1
            vx,vy = u*distance,u*distance

        else:
            vx,vy = me.vectTo(uo)
            vx *= distance/me.distanceTo(uo)
            vy *= distance/me.distanceTo(uo)

        for i,hero in zip(range(1,4),heros):
            theta = (np.pi/2)* i/(len(heros)+1)
            hero.x0,hero.y0 = int(vx*np.cos(theta) + base_x),int(vy*np.sin(theta) + base_y)

    def update_comportement(self,heros ,distance):
        if distance <= 5000 :
            comportements = [
                DefenseIntensive,
                DefenseWind,
                DefenseInterneOpti,
                DefenseHeroShield,
                DefenseAdvRedirection,
                Wait
            ]
        else :# distance <= 9000:
            comportements = [
                DefenseExterne,
                DefenseRedirection,
                DefenseInterneOpti,
                DefenseHeroShield,
                DefenseAdvRedirection,
                Wait
            ]
        print(f"Comportement de {len(heros)} heros",file=sys.stderr)
        for hero in heros:
            hero.comportements = comportements

    def update(self):
        distances = [0,2000,6000,12000,20000]
        for distance0,distance1,i in zip(distances[:-1],distances[1:],range(1,4)):
            filtre = lambda hero: distance0 < hero.distanceTo(me) < distance1
            heros = list(filter(filtre, self))
            self.update_positionnement(heros, distances[i])
            self.update_comportement(heros, distances[i])


    def is_target(self,monstre) -> bool :
        return monstre in [hero.cible for hero in self]

    def initHero(self,_id,x, y, shield_life, is_controlled):
        hero = Hero(_id,x,y,shield_life,is_controlled)
        self.heros[_id] = hero
        
    def initEnd(self):
        self.update_positionnement(list(self),6000)

#### LOOP #################################################################################
#%%
heros = Heros()
monstres = Monstres()
# game loop
firstRound = True
while True:
    monstres = Monstres()
    H=[] #Position des heroes
    health1, mana1 = [int(j) for j in input().split()]
    health2, mana2 = [int(j) for j in input().split()]
    
    mana = mana1 if id_joueur == 1 else mana2
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
            monstres.addMonster(_id, Monstre(_id,x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))   

        elif _type == 1:
            if heros.heros.get(str(_id)):
                heros.heros[str(_id)].update(x, y, shield_life, is_controlled)
                #print(f"Hero {str(_id)} 's target", heros[str(_id)].cible,file = sys.stderr )
            else:
                heros.initHero(str(_id),x, y, shield_life, is_controlled)

        elif _type == 2:
            if adversaires.adversaires.get(str(_id)):
                adversaires.adversaires[str(_id)].update(x, y, shield_life, is_controlled)

            else:
                adversaires.initAdversaire(str(_id), x, y, shield_life, is_controlled)

    if firstRound:
        heros.initEnd()
    monstres.update()
    me.update()
    uo.update()
    heros.update()
    print(f"Dangerosite : {me.dangerosite0} || Evolution  {me.evolution}",file=sys.stderr)
    for hero in heros:
        hero.update_around()
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        m = hero.play()
        if type(m) == int: 
            mana -=m
    del monstres 