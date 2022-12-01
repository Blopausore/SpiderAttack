#start-of-file

class Hero(Entitee):
    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(x, y)
        self.id = id
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.cible = EntiteeNull()
        self.around = [EntiteeNull()]
        self.x0 = x
        self.y0 = y
        self.reactions = [] #Pile de comportement employe qu'une fois
        self.zone_filtre = zones[int(id) % 3]
        self.comportements = [
            DefenseHeroShield
        ]


    def __str__(self):
        return "Hero"

    def __iter__(self):
        return iter([self])

    def __next__(self):
        return next(self)

    def update_around(self,reverse = False):
        self.around = list(sorted(monstres,key = lambda m : self.distanceTo(m)))        

    def update_around(self,reverse = False):
        self.around = list(sorted(monstres,key = lambda m : self.distanceTo(m)))        

    def next_around(self):

        filtre = lambda monstre : monstre.distanceTo(me) < 1600
        self.around = list(sorted(filter(
            filtre,monstres.next_moves()),
            key = lambda m : m.distanceTo(me)))


    def position_opti_v1(self):
        opti = EntiteeNull()
        nb_opti = 0
        for i, m1 in enumerate(self.around[:-1]):
            for m2 in self.around[i+1:]:
                if m1.distanceTo(m2) < 1600:
                    potentiel = Entitee((m1.x+m2.x)//2,(m1.y+m2.y)//2)
                    filtre = lambda m : m.distanceTo(potentiel)
                    nb = sum(filter(filtre, self.around))
                    if nb_opti < nb:
                        opti = potentiel
                        nb_opti = nb
        return opti
                    
    def position_opti(self,key_ = lambda m : m.distanceTo(me)):
        if len(self.around) == 0: return EntiteeNull()
        if len(self.around) == 1: return self.around[0]
        opti = EntiteeNull()
        nb_opti = 0
        m1 = self.around[0]
        for m2 in self.around[1:]:
            if m1.distanceTo(m2) < 1600:
                potentiel = Entitee((m1.x+m2.x)//2,(m1.y+m2.y)//2)
                filtre = lambda m : m.distanceTo(potentiel)
                nb = len(list(filter(filtre, self.around)))
                if nb_opti < nb:
                    opti = potentiel
                    nb_opti = nb
        return opti

                    
    def update(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield_life= shield_life
        self.is_controlled = is_controlled
        self.update_around()

    def shield_off(self):
        return self.shield_life == 0

    def entiteeClosest(self,filtre=identitee,entitees=monstres):
        for entitee in sorted(filter(filtre, entitees),key = lambda e : self.distanceTo(e)):
            return entitee
        return EntiteeNull()

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

