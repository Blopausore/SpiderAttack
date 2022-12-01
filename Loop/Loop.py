
#start-of-file

while True:
    monstres = Monstres()
    H=[] #Position des heroes
    health1, mana1 = [int(j) for j in input().split()]
    health2, mana2 = [int(j) for j in input().split()]
    
    mana = mana1 if id_joueur == 1 else mana2
    entity_count = int(input())  # Amount of heros and monsters you can see

    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0 = monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
       
        if _type == 0: 
            monstres.addMonster(_id, Monstre(_id,x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))   

        elif _type == 1:
            if heros.heros.get(str(_id)):
                heros.heros[str(_id)].update(x, y, shield_life, is_controlled)
                #print(f"Hero {str(_id)} 's target", heros[str(_id)].cible,file = sys.stderr )
            else:
                heros.initHero(str(_id),x, y, shield_life, is_controlled)

        elif _type == 2:
            if adversaires.adversaires.get(str(_id)):
                adversaires.adversaires[str(_id)].update(x, y, shield_life, is_controlled)

            else:
                adversaires.initAdversaire(str(_id), x, y, shield_life, is_controlled)

    if firstRound:
        heros.initEnd()
    monstres.update()
    me.update()
    uo.update()
    heros.update()
    print(f"Dangerosite : {me.dangerosite0} || Evolution  {me.evolution}",file=sys.stderr)
    for hero in heros:
        hero.update_around()
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        m = hero.play()
        if type(m) == int: 
            mana -=m
    del monstres 
    