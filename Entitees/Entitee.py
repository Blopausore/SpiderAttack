#start-of-file

class Entitee:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def update(self,x,y):
        self.x = x
        self.y = y

    def distanceTo(self,other):
        return N(self.x,self.y,other.x,other.y)

    def vectTo(self,other):
        return (other.x - self.x, other.y - self.y)

    def isNull(self):
        return False

    
class EntiteeNull():
    def __init__(self):
        self.x = 1e10
        self.y = 1e10

    def isNull(self):
        return True
    def __str__(self):
        return "EntiteeNull"
