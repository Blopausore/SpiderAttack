#start-of-file

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

    def __init__(self,hero):
        super().__init__(hero)
        self.vhx,self.vhy = hero.vectTo(me)

    def __str__(self):
        return "DefenseInterneOpti"

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
