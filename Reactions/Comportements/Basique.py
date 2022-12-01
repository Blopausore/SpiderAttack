#start-of-file

class Wait(Comportement):

    def __str__(self):
        return "WAIT"
    
    def action(self):
        print("MOVE",self.hero.x0,self.hero.y0,"WAIT ")
        return True
        
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

class AttaqueAround(Comportement):
    def __str__(self):
        return "AttaqueAround"

    def action(self):
        monstre = self.hero.position_opti() 
        if not monstre.isNull():
            return self.attaque(monstre)
        return False