from minihack import LevelGenerator


def create_level(width: int, height: int, monsters = [], traps = [], weapons = [], potion = False, armor = False):

    lvl = LevelGenerator(w=width, h=height)

    lvl.wallify()

    for monster in monsters:
        lvl.add_monster(name = monster)

    for trap in traps:
        lvl.add_trap(name = trap)

    for weapon in weapons:
        lvl.add_object(name = weapon, symbol=')')
    
    if potion:
        lvl.add_object(name = "full healing", symbol = "!")
    
    if armor:
        lvl.add_object(name = "leather armor", symbol = "[")

    return lvl.get_des()

H = 15
W = 15
NUM_EPISODES = 1
MAX_STEPS = 200
MONSTER = ['giant bat', 'kobold']
WEAPON = []

with open("skill_combat.des","w") as f:
    f.write(create_level(width = W, height = H, monsters = MONSTER, weapons = WEAPON, potion = True, armor = False))