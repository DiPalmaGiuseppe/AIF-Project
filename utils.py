import matplotlib.pyplot as plt
import IPython.display as display
import time
import re
from pyswip import Prolog
from minihack import LevelGenerator
from minihack import RewardManager

def create_level(width: int, height: int, monsters = [], traps = [], weapons = [], potion = False, armor = False):

    lvl = LevelGenerator(w=width, h=height)

    lvl.wallify()

    for monster in monsters:
        lvl.add_monster(name = monster)

    for trap in traps:
        lvl.add_trap(name = trap)

    for weapon in weapons:
        lvl.add_weapon(name = weapon)
    
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
    if 'pick' in action: 
        action_id = 49
        classObject = re.search(r"pick\((.*?)\)", action)
        
        if classObject == "potion":
            kb.retractall(f'stepping_on(agent, potion, health)')
            obs, _, _, _ = env.step(action_id)
            mapped_key = bytes(obs['message']).decode('utf-8').rstrip('\x00').split('-')[0].replace(" ", "")
            kb.asserta(f'has(agent, potion, health, {mapped_key})')
            return None
        else classObject == "weapon":
            pass
        
    elif action == 'wield': action_id = 78
    elif 'northeast' in action: action_id = 4
    elif 'southeast' in action: action_id = 5
    elif 'southwest' in action: action_id = 6
    elif 'northwest' in action: action_id = 7
    elif 'north' in action: action_id = 0
    elif 'east' in action: action_id = 1
    elif 'south' in action: action_id = 2
    elif 'west' in action: action_id = 3
    
    elif 'drink' in action:
        mapped_key = re.search(r"drink\((.*?)\)", action).group(1)
        action_id = 52
        kb.retractall(f'has(agent, potion, health, {mapped_key})')
        obs, _, _, _ = env.step(action_id)
        message = bytes(obs['message']).decode('utf-8').rstrip('\x00')
        action_id = env.actions.index(ord(mapped_key))

    # print(f'Action performed: {repr(env.actions[action_id])}')
    return env.step(action_id)

def process_state(obs: dict, kb: Prolog, monsters, weapons = []):
    kb.retractall("position(_,_,_,_)")
    kb.retractall("stepping_on(_,_,_)")
    kb.retractall("health(_)")

    for i in range(21):
        for j in range(79):
            if not (obs['screen_descriptions'][i][j] == 0).all():
                obj = bytes(obs['screen_descriptions'][i][j]).decode('utf-8').rstrip('\x00')
                if 'wall' == obj:
                    kb.asserta(f'position(wall, _, {i}, {j})')
                if 'corpse' in obj:
                    kb.asserta(f'position(trap, _, {i}, {j})')
                elif 'sword' in obj:
                    kb.asserta(f'position(weapon, {weapon}, {i}, {j})')
                elif 'potion' in obj:
                    kb.asserta(f'position(potion, health, {i},{j})')

                for monster in monsters:
                    if monster == obj:
                        kb.asserta(f'position(enemy, {monster.replace(" ", "")}, {i}, {j})')

    message = bytes(obs['message']).decode('utf-8').rstrip('\x00')
    if 'You see here' in message:
        if 'potion' in message:
            kb.asserta('stepping_on(agent, potion, health)')
        elif 'long word' in message:
            kb.asserta('stepping_on(agent, weapon, tsurugi)')

    for item in obs["inv_strs"]:
        obj = bytes(item).decode('utf-8').rstrip('\x00')
        if 'katana' in obj:
            kb.asserta("has(agent, weapon, katana, a)")
        if 'tsurugi' in obj:
            kb.asserta("has(agent, weapon, tsurugi, b)")

    kb.asserta(f"position(agent, _, {obs['blstats'][1]}, {obs['blstats'][0]})")
    kb.asserta(f"health({int(obs['blstats'][10]/obs['blstats'][11]*100)})")

# indexes for showing the image are hard-coded
def show_match(states: list):
    image = plt.imshow(states[0][20:300, 480:775])
    for state in states[1:]:
        display.display(plt.gcf())
        display.clear_output(wait=True)
        image.set_data(state[20:300, 480:775])
    display.display(plt.gcf())
    display.clear_output(wait=True)