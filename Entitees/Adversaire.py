#start-of-file

class Adversaire(Entitee):
    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(x, y)
        self.id = id
        self.shield_life = shield_life
        self.is_controlled = is_controlled

    def __str__(self):
        return "Adversaire"

    def update(self, x, y, shield_life, is_controlled):
        self.x = x
        self.y = y
        self.shield_life = shield_life
        self.is_controlled = is_controlled

    def shield_off(self):
        return self.shield_life == 0

