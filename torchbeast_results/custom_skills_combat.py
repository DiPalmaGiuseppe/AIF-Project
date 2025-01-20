from minihack import MiniHackSkill
from minihack.envs import register

from minihack import RewardManager

def define_reward(monsters):
    reward_manager = RewardManager()

    for monster in monsters:
        reward_manager.add_kill_event(name=monster, reward=1, terminal_required = True, terminal_sufficient = False)

    return reward_manager

# HYDRA_FULL_ERROR=1 python3 -m minihack.agent.polybeast.polyhydra model=baseline env=MiniHack-Combat-Skill-v0 total_steps=500000 > output.txt 2> output_err.txt
# TEST 1: MONSTER = ['goblin', 'kobold'] // all tests done
# TEST 2: MONSTER = ['bat', 'giant bat'] // all tests done
# TEST 3: MONSTER = ['giant bat', 'kobold'] // all tests done
# TEST 4: MONSTER = ['giant bat', 'goblin', 'kobold'] // all tests done
# TEST 5: MONSTER = ['bat', 'giant bat', 'kobold']

MONSTER = ['bat', 'giant bat', 'kobold']

class MiniHackCombatSkill(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        kwargs["character"] = "sam-hum-neu-mal"
        reward_manager = define_reward(MONSTER)
        super().__init__(*args, des_file="skill_combat.des", reward_manager = reward_manager, **kwargs)

register(
    id="MiniHack-Combat-Skill-v0",
    entry_point="minihack.envs.custom_skills_combat:MiniHackCombatSkill",
)