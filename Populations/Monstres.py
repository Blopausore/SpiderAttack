#start-of-file

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

    def next_moves(self,n=1):
        return map(lambda monstre : monstre.next_move(n),self)

