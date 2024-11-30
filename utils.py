import matplotlib.pyplot as plt
import IPython.display as display
import time
from pyswip import Prolog
from minihack import LevelGenerator
from minihack import RewardManager

def create_level(width: int, height: int, monsters = [], traps = [], weapons = [], potion = False):

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

    return lvl.get_des()

def define_reward(monsters):
    reward_manager = RewardManager()

    for monster in monsters:
        reward_manager.add_kill_event(name=monster, reward=1, terminal_required = True, terminal_sufficient = False)

    return reward_manager

def perform_action(action, env, kb):
    action_id = -1
    if action == 'pick': 
        action_id = 49
        kb.retractall(f'stepping_on(agent, potion, health)')
        kb.asserta(f'has(agent, potion, health)')
        
    elif action == 'wield': action_id = 78
    elif 'northeast' in action: action_id = 4
    elif 'southeast' in action: action_id = 5
    elif 'southwest' in action: action_id = 6
    elif 'northwest' in action: action_id = 7
    elif 'north' in action: action_id = 0
    elif 'east' in action: action_id = 1
    elif 'south' in action: action_id = 2
    elif 'west' in action: action_id = 3

    return env.step(action_id)

def process_state(obs: dict, kb: Prolog, monsters, weapons = []):
    kb.retractall("position(_,_,_,_)")

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

    kb.retractall("position(agent,_,_,_)")
    kb.retractall("health(_)")
    kb.asserta(f"position(agent, _, {obs['blstats'][1]}, {obs['blstats'][0]})")
    kb.asserta(f"health({int(obs['blstats'][10]/obs['blstats'][11]*100)})")

# indexes for showing the image are hard-coded
def show_match(states: list):
    image = plt.imshow(states[0][90:290, 481:750])
    for state in states[1:]:
        time.sleep(0.25)
        display.display(plt.gcf())
        display.clear_output(wait=True)
        image.set_data(state[90:290, 481:750])
    time.sleep(0.25)
    display.display(plt.gcf())
    display.clear_output(wait=True)