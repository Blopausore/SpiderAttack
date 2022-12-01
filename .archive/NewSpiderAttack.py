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
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.cible = MonstreNull()
        self.around = [MonstreNull()]
        self.x0 = x
        self.y0 = y
        self.comportements = []
        self.reactions = [] #Pile de comportement employe qu'une fois

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
            action = comportement.action()
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

    def attaque(self, mc): #mc : monstre cible
        print(f"MOVE {mc.x} {mc.y}")
        return True

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


##Action basique
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

class AttaqueClosest(Comportement):
    def __init__(self,hero,filtre = identitee,cibler = False):
        super().__init__(hero)
        self.filtre = filtre    
        self.cibler = cibler

    def __str__(self):
        return "Attaquelosest"

    def action(self):
        for monstre in filter(self.filtre, self.hero.around):
            if self.cibler : self.setCible(monstre)
            return self.attaque(monstre)
        return False


## Defense basique
class DefenseInterieur(Comportement):
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

class DefenseExterieur(Comportement):
    def __str__(self):
        return "DefenseExterieur"

    def posInitial(self):
        vx,vy = me.vectTo(centre)
        self.hero.x0 = me.x + vx*3//4
        self.hero.y0 = me.y + vy*3//4

    def action(self):
        self.posInitial()
        filtre = lambda m : m.threat_for == 1 and not m.near_base and m.distance < 12000
        for monstre in filter(filtre, self.hero.around):
            if not heros.is_target(monstre):
                self.setCible(monstre)
                return self.attaque(monstre)

        for monstre in filter(filtre, self.hero.around):
            self.setCible(monstre)
            return self.attaque(monstre)
        return False

class DefenseWind(Comportement):
    def __init__(self,hero,distance):
        super().__init__(hero)
        self.distance = distance

    def __str__(self):
        return "DefenseWind"

    def action(self):
        filtre = lambda m : m.shield_off() and m.distance < self.distance and m.health > 5 and m.danger
        for monstre in filter(filtre,monstres.closests):
            return self.wind(monstre,xc,yc) 
        return False

##Defense test

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

## SPELL

class ControlAdv(Comportement):
    def __str__(self):
        return "ControlAdversaire"
    def __init__(self,hero,x,y):
        super().__init__(hero)
        self.x = x
        self.y = y

    def action(self):
        key_ = lambda adversaire : adversaire.distanceTo(self.hero)
        for adversaire in sorted(adversaires,key=key_):
            if self.control(adversaire,self.x,self.y):
                return 10
        return False


class AttaqueControl(Comportement):
    def __str__(self):
        return "AttaqueControl"

    def action(self):
        filtre = lambda m : m.threat_for == 1 and not m.near_base and m.shield_off()
        for monstre in filter(filtre,monstres.closests):
            if self.control(monstre,uo.x,uo.y):
                return 10
        return False


class ControlSpider(Comportement):
    def __str__(self):
        return "ControlSpider"
    def action(self):
        filtre = lambda m : m.threat_for == 2 and m.distanceTo(uo) < 6000 and m.shield_off()
        for monstre in filter(filtre,monstres.closests):
            if self.shield(monstre):
                return 10
        return False

###REACTION
class DefenseControl(Comportement):
    def __str__(self):
        return "DefenseControl"
    def condition_self_shield(self):
        return self.hero.shield_off()

    def action(self):
        if self.condition_self_shield():
            return self.shield(self.hero)
        
        for hero in heros:
            if self.hero != hero:
                if self.shield(hero):
                    return 10
        return False

##### COMBO ######################################################################

class Combo:
    def __init__(self):
        pass

    def __iter__(self):
        return iter(self)

    def __next__(self):
        return next(self)

class EnemyControl(Combo):
    def __init__(self):
        self.comportements = [
            [DefenseControl,DefenseControl],
            [DefenseControl,DefenseControl],
            [DefenseControl,DefenseControl]
        ]

    def __iter__(self):
        return zip(heros,self.comportements)


class DefenseSpiderShield(Combo):
    def __init__(self,nb):
        self.comportements = [
            [DefenseInterneOpti],
            [DefenseInterneOpti],
            [DefenseInterneOpti]
        ]
        self.heros = [hero for _,hero in zip(range(nb),sorted(heros,key = lambda hero : hero.distanceTo(me)))]

    def __iter__(self):
        return zip(self.heros,self.comportements)


class AttaqueVicieuse(Combo):
    def __init__(self):
        self.comportements = [
            [DefenseControl],
            [DefenseControl],
        ]

class DefenseInvasion(Combo):
    def __init__(self):
        controldAdv = lambda hero : ControlAdv(hero,uo.x,uo.y)
        self.comportements = [
            [controldAdv],
            [controldAdv],
            [controldAdv]
        ]

    def __iter__(self):
        return zip(heros,self.comportements)




#### CLASS HEROS #################################################################################
#%%
class Heros:
    def __init__(self):
        self.heros = {}
        self.evenements = [
            self.EnemyControl,
            self.InvasionAdv,
            self.SpiderShield,
            self.ControlSpider
        ]

    def __iter__(self):
        return iter(self.heros.values())

    def __next__(self):
        return next(self)

    def is_target(self,monstre) -> bool :
        return monstre in [hero.cible for hero in self]

    def initHero(self,_id,x, y, shield_life, is_controlled):
        hero = Hero(_id,x,y,shield_life,is_controlled)
        level = int(_id)%3
        if level == 0:
            hero.comportements.append(DefenseWind(hero,2000))
            hero.comportements.append(AttaqueCible(hero))
            hero.comportements.append(DefenseInterneOpti(hero))
        elif level in [1,2]:
            hero.x0 = xc
            hero.y0 = level * ymax//3
            hero.comportements.append(DefenseExterieur(hero))
            hero.comportements.append(AttaqueCible(hero))
            filtre_chasse = lambda m : not self.is_target(m)
            hero.comportements.append(AttaqueClosest(hero,filtre=filtre_chasse,cibler=True))

        hero.comportements.append(Wait(hero))
        self.heros[_id] = hero
    
    def comboAdd(self,combo):
        for hero,reactions in combo:
            hero.reactions = reactions


##EVENEMENTS##
    def EnemyControl(self):
        if sum([hero.is_controlled for hero in heros]) > 0:
            self.comboAdd(EnemyControl())
            return True
        return False

    def SpiderShield(self):
        filtre = lambda m : not m.shield_off() and m.danger
        monstres_shield = list(filter(filtre,monstres)) 
        if monstres_shield:
            max_health = max([monstre.health for monstre in monstres_shield])
            if max_health >= 10:
                self.comboAdd(DefenseSpiderShield(max_health//10))
            return True
        return False

    def InvasionAdv(self):
        key_ = lambda adversaire : adversaire.distanceTo(me)
        for adversaire in sorted(adversaires, key=key_):
            if adversaire.distanceTo(me) < 8000:
                self.comboAdd(DefenseInvasion())
                return True
        return False

    def ControlSpider(self):
        if monstres.maxhealth > 18 : 
            for hero in heros:
                hero.comportements.insert(0,AttaqueControl(hero))
            self.delEvenements(ControlSpider)
            return True
        return False

    def delEvenements(self,evenement):
        for i,eventListe in enumerate(map(str,self.evenements)):
            if eventListe == str(evenement):
                del self.evenements[i]
                
    def check_evenements(self):
        for evenement in self.evenements:
            if evenement():
                return True
        return False

    def update(self):
        if me.evolution >= 3:
            for hero in self:
                if not "DefenseWind" in list(map(str,hero.comportements)):
                    hero.comportements.insert(0,DefenseWind(hero,3000))
                    break
                elif not "DefenseInterneOpti" in list(map(str,hero.comportements)):
                    hero.comportements.insert(0,DefenseInterneOpti(hero))
                    break

        if me.evolution <= -3:
            key_ = lambda hero : hero.distanceTo(uo)
            for hero in sorted(self,key=key_):
                if DefenseInterneOpti(hero) in hero.comportements:
                    del hero.comportements[hero.comportements.index(DefenseInterneOpti(hero))]
                    break

    
        if self.check_evenements():
            return True




#### LOOP #################################################################################
#%%
heros = Heros()
monstres = Monstres()
# game loop
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