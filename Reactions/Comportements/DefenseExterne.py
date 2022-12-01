#start-of-file

class DefenseExterne(Comportement):
    def __str__(self):
        return "DefenseExterieur"

    def action(self):
        filtre = lambda m : m.threat_for == 1 and not m.near_base and m.distance < 12000 and self.hero.zone_filtre(m)
        monstre_around = self.hero.entiteeClosest(filtre,monstres)
        if not monstre_around.isNull():
            return self.attaque(monstre_around)
        return False

class DefenseRedirection(Comportement):
    def __str__(self):
        return "DefenseRedirection"

    def action(self):
        filtre = lambda m : m.threat_for == 1 and not m.near_base and m.health > 25 and m.shield_off()
        monstre_around = self.hero.entiteeClosest(filtre,monstres)
        if not monstre_around.isNull():
            return self.control(monstre_around,uo.x,uo.y)

class Chasse(Comportement):
    def __str__(self):
        return "Chasse"

    def action(self):
        filtre = lambda m : self.hero.zone_filtre(m)
        monstre_around = self.hero.entiteeClosest(filtre,monstres)
        if not monstre_around.isNull():
            return self.attaque(monstre_around)
        return False
       