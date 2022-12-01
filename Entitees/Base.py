#start-of-file

class Base(Entitee):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.counter_near = 0
        self.counter_potentiel = 0
        self.evolution = 0
        self.dangerosite0 = 0
        self.dangerosite1 = 0

    def __str__(self):
        return "Base"
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