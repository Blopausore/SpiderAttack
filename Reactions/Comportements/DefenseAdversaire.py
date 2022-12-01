#start-of-file

class DefenseAdvRedirection(Comportement):
    def __str__(self):
        return "DefenseAdvRedirection"

    def action(self):
        key_ = lambda adversaire : adversaire.distanceTo(self.hero)
        filtre = lambda adversaire : self.hero.distanceTo(me) > adversaire.distanceTo(me) 
        if not self.hero.cible.isNull() and str(self.hero.cible) == "Adversaire":
            if self.control(self.hero.cible,uo.x,uo.y):
                return 10
            self.hero.cible = EntiteeNull()

        for adversaire in filter(filtre,sorted(adversaires,key=key_)):
            if self.control(adversaire,uo.x,uo.y):
                self.hero.cible = adversaire
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
        filtre = lambda monstre : monstre.danger and monstre.health > 5 and monstre.distanceTo(me)
        monstres_around = self.hero.entiteeClosest(filtre,monstres)
        if not monstres_around.isNull():
            return self.attaque(monstres_around)
