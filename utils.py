import matplotlib.pyplot as plt
import IPython.display as display
import time
import re
from pyswip import Prolog
from minihack import LevelGenerator
from minihack import RewardManager

inventory_key = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
inventory_weapon = ['katana','wakizashi','tsurugi','bow', 'axe','two-handed sword', 'yumi']


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

def define_reward(monsters):
    reward_manager = RewardManager()

    for monster in monsters:
        reward_manager.add_kill_event(name=monster, reward=1, terminal_required = True, terminal_sufficient = False)

    return reward_manager

def perform_action(action, env, kb):
    action_id = -1

    if 'shoot' in action:
        action_id = 34
        direction = re.search(r"shoot\((.+)\)", action).group(1)
        obs, _, _, _ = env.step(action_id)
        action = direction

    if 'pick' in action: 
        action_id = 49
        return None
        
    elif 'wield' in action:
        action_id = 78
        mapped_key = re.search(r"wield\((.)\)", action).group(1)
        obs, _, _, _ = env.step(action_id)
        action_id = env.actions.index(ord(mapped_key))

    elif 'northeast' in action: action_id = 4
    elif 'southeast' in action: action_id = 5
    elif 'southwest' in action: action_id = 6
    elif 'northwest' in action: action_id = 7
    elif 'north' in action: action_id = 0
    elif 'east' in action: action_id = 1
    elif 'south' in action: action_id = 2
    elif 'west' in action: action_id = 3
    
    elif 'drink' in action:
        action_id = 52
        mapped_key = re.search(r"drink\((.)\)", action).group(1)
        obs, _, _, _ = env.step(action_id)
        action_id = env.actions.index(ord(mapped_key))

    # print(f'Action performed: {repr(env.actions[action_id])}')
    return env.step(action_id)

def process_state(obs: dict, kb: Prolog, monsters):
    kb.retractall("position(_,_,_,_)")
    kb.retractall("stepping_on(_,_,_)")
    kb.retractall("wields_weapon(_,_)")
    kb.retractall("has(_,_,_,_)")
    kb.retractall("health(_)")

    for i in range(21):
        for j in range(79):
            if not (obs['screen_descriptions'][i][j] == 0).all():
                obj = bytes(obs['screen_descriptions'][i][j]).decode('utf-8').rstrip('\x00')
                if 'wall' == obj:
                    kb.asserta(f'position(wall, _, {i}, {j})')
                elif 'corpse' in obj:
                    kb.asserta(f'position(trap, _, {i}, {j})')
                elif 'potion' in obj:
                    kb.asserta(f'position(potion, _, {i},{j})')
                elif "sword" in obj:
                    kb.asserta(f'position(weapon, sword, {i}, {j})')
                elif "bow" in obj:
                    kb.asserta(f'position(weapon, bow, {i}, {j})')
                elif "armor" in obj:
                    armor_material = re.search(r"a (\w+) armor", obj).group(1)
                    kb.asserta(f'position(armor, {armor_material}, {i}, {j})')

                for monster in monsters:
                    if monster == obj:
                        kb.asserta(f'position(enemy, {monster.replace(" ", "")}, {i}, {j})')

    message = bytes(obs['message']).decode('utf-8').rstrip('\x00')
    if 'You see here' in message:
        if 'potion' in message:
            potion_color = re.search(r"You see here an? ([\w\-]+\ ?[\w\-]*) potion", message).group(1)
            kb.asserta(f'stepping_on(agent, potion, {potion_color.replace(" ", "")})')
        elif 'tsurugi' in message:
            kb.asserta('stepping_on(agent, weapon, tsurugi)')
        elif 'bow' in message:
            kb.asserta('stepping_on(agent, weapon, bow)')


    # print("-----------INVENTORY----------------")
    for i, item in enumerate(obs["inv_strs"]):
        obj = bytes(item).decode('utf-8').rstrip('\x00')
        if obj != '':
            # print(f"{inventory_key[i]}: {obj}")
            for weapon in inventory_weapon:
                if weapon in obj:
                    kb.asserta(f"has(agent, weapon, {weapon}, {inventory_key[i]})")    
                    if 'weapon in hand' in obj:
                        kb.asserta(f"wields_weapon(agent, {weapon})")

            if 'potion' in obj:
                potion_color = re.search(r"an? ([\w\-]+\ ?[\w\-]*) potion", message).group(1)
                kb.asserta(f"has(agent, potion, {potion_color}, {inventory_key[i]})")

    # print(f"HEALTH: {int(obs['blstats'][10]/obs['blstats'][11]*100)}")

    kb.asserta(f"position(agent, _, {obs['blstats'][1]}, {obs['blstats'][0]})")
    kb.asserta(f"health({int(obs['blstats'][10]/obs['blstats'][11]*100)})")
    

# indexes for showing the image are hard-coded
def show_match(states: list):
    image = plt.imshow(states[0][20:300, 480:775])
    for state in states[1:]:
        display.display(plt.gcf())
        display.clear_output(wait=True)
        image.set_data(state[20:300, 480:775])
        # time.sleep(.75)
    display.display(plt.gcf())
    display.clear_output(wait=True)
    # time.sleep(.75)
