class Heros:
    def __init__(self):
        self.cibles=[]
        self.pos=[]



class Hero:
    def __init__(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield = shield_life
        self.controlled = is_controlled
        self.cible = "-1"
        self.around = []
        self.x0 = x
        self.y0 = y

    def update(self,x,y,shield_life,is_controlled):
        self.x = x
        self.y = y
        self.shield = shield_life
        self.controlled = is_controlled

    def around_him(self,monstres,distance): #Renvoi les menaces les plus proches du hero
        l=[]
        for _id,m in monstres.monstres.items():
            d=N(self.x,self.y,m.x,m.y)
            if  d <= distance and m.threat_for == 1:
                l.append([d,_id])      
        
        self.around = [ _id for _,_id in sorted(l)]
            
    def attack(self,monstres):

        if self.cible in monstres.dangerous :
            mc = monstres.monstres[self.cible]
            print("MOVE",mc.x,mc.y, "Continue attacking his target")
            return True
        return False
        
    def wait(self):
        print("MOVE",self.x0,self.y0,"WAIT : ")
        return True

    def spell(self,monsters,mana):
        pass

class Defenseur(Hero):

    def attack(self,monstres):
        if not super().attack(monstres):
            for dist in range(100,1000,100):
                self.around_him(monstres,dist)
                if self.around:
                    self.cible = self.around[0]
                    mc = monstres.monstres[self.cible]
                    print("MOVE",mc.x,mc.y, "Attack around")
                    return True
            if monstres.dangerous:
                self.cible = monstres.dangerous.pop()
                mc = monstres.monstres[self.cible]
                print("MOVE",mc.x,mc.y,"Attack danger")
                return True

        return False


class Eclaireur(Hero):
    def __init__(self,x,y,shield_life,is_controlled):
        super().__init__(x,y,shield_life,is_controlled)
        self.x0 = base_x + (xc - base_x)//2
        self.y0 = base_y + (yc - base_y)//2



    def attack(self,monstres):

        if not super().attack(monstres):
            for dist in range(100,600,100):
                self.around_him(monstres,dist)
                if self.around:
                    self.cible = self.around[0]
                    mc = monstres.monstres[self.cible]
                    print("MOVE",mc.x,mc.y,"Attack around"+self.cible)
                    return True
            if monstres.potentiels:
                self.cible = monstres.potentiels.pop()
                mc = monstres.monstres[self.cible]
                print("MOVE",mc.x,mc.y,"Attack potential"+self.cible)
                return True
        return False

