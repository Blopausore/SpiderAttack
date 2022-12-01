#start-of-file


class Heros:
    def __init__(self):
        self.heros = {}
        
    def __iter__(self):
        return iter(self.heros.values())

    def __next__(self):
        return next(self)
    
    def update_positionnement(self, heros ,distance):
        if distance < 10000:
            if distance < 5000 and len(list(filter(lambda m : m.danger,monstres))) == 0 :
                distance = 6000
            u = 1 if id_joueur == 1 else -1
            vx,vy = u*distance,u*distance

        else:
            vx,vy = me.vectTo(uo)
            vx *= distance/me.distanceTo(uo)
            vy *= distance/me.distanceTo(uo)

        for i,hero in zip(range(1,4),heros):
            theta = (np.pi/2)* i/(len(heros)+1)
            hero.x0,hero.y0 = int(vx*np.cos(theta) + base_x),int(vy*np.sin(theta) + base_y)

    def update_comportement(self,heros ,distance):
        nbProche = 0
        for i,hero in enumerate(heros):
            
            if nbProche < 2 and distance <= 5500 :
                nbProche+=1
                comportements = [
                    DefenseHeroShield,
                    DefenseWind,
                    DefenseInterne,
                    AttaqueAround,
                    DefenseInterneOpti,
                    DefenseAdvRedirection,
                    Wait
                ]
            else:# distance <= 9000:
                comportements = [
                    DefenseHeroShield,
                    DefenseInterne,
                    DefenseRedirection,
                    DefenseExterne,
                    DefenseAdvRedirection,
                    AttaqueAround,
                    Chasse,
                    Wait
                ]
            hero.comportements = comportements


        

    def update(self):
        distances = [0,2000,6000,12000,20000]
        for distance0,distance1,i in zip(distances[:-1],distances[1:],range(1,4)):
            filtre = lambda hero: distance0 < hero.distanceTo(me) < distance1
            heros = list(filter(filtre, self))
            self.update_positionnement(heros, distances[i])
            self.update_comportement(heros, distances[i])


    def is_target(self,monstre) -> bool :
        return monstre in [hero.cible for hero in self]

    def initHero(self,_id,x, y, shield_life, is_controlled):
        hero = Hero(_id,x,y,shield_life,is_controlled)
        self.heros[_id] = hero


    def initEnd(self):
        self.update_positionnement(list(self),6000)


