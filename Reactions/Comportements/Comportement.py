#start-of-file

class Comportement:
    def __init__(self,hero):
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

    def attaque_opti(self):
        pos_opti = self.hero.position_opti() 
        if not pos_opti.isNull():
            return self.attaque(pos_opti)
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
