#start-of-file

class Adversaires:
    def __init__(self):
        self.adversaires = {}

    def __iter__(self):
        return iter(self.adversaires.values())

    def __next__(self):
        return next(self)

    def initAdversaire(self,_id,x, y, shield_life, is_controlled):
        self.adversaires[_id] = Adversaire(_id, x, y, shield_life, is_controlled)
   