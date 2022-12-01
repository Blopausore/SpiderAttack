#start-of-file

class Defense(Hero):
    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(id, x, y, shield_life, is_controlled)
        self.x0 
        self.y0
        self.comportements.extend([
            DefenseWind,
            DefenseInterne,
            AttaqueAround,
            DefenseInterneOpti,
            DefenseAdvRedirection,
            Wait
        ]) 
