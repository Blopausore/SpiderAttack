#start-of-file
class AttaqueShield(Comportement):
    def __str__(self):
        return "AttaqueShield"

    def action(self):
        filtre = lambda m : m.shield_off() and m.threat_for == 2 and m.near_base
        monstre = self.hero.entiteeClosest(filtre,monstres)
        if not monstre.isNull():
            return self.shield(monstre)
        return False

class AttaqueWind(Comportement):
    def __str__(self):
        return "AttaqueWind"

    def action(self):
        filtre = lambda m : m.threat_for != 2
        monstre = self.hero.entiteeClosest(filtre,monstres)
        if not monstre.isNull():
            return self.wind(monstre,uo.x,uo.y)
        return False
    
class AttaqueControl(Comportement):
    def __str__(self):
        return "AttaqueControl"

    def action(self):
        filtre = lambda adv : adv.distanceTo(uo) < 5000 and len(monstres.allies) > 0
        adversaire = self.hero.entiteeClosest(filtre,adversaires)
        if not adversaire.isNull():
            return self.control(adversaire,centre.x,centre.y)
        return False
