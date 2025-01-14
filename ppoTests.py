from minihack import MiniHackNavigation
from nle import nethack

class CustomMiniHackEnv(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        super().__init__(
            des_file="custom_map.des",  # Path to your .des file
            max_episode_steps=100,
            reward_win=1,
            reward_lose=-1,
            *args,
            **kwargs,
        )

    def step(self, action):
        obs, reward, done, info = super().step(action)
        # Customize the reward if needed
        return obs, reward, done, info

    def reset(self):
        return super().reset()

# Register the environment
from gymnasium.envs.registration import register

register(
    id="CustomMiniHack-v0",
    entry_point="__main__:CustomMiniHackEnv",
)


import gymnasium as gym
from stable_baselines3 import PPO

# Create the environment
env = gym.make("CustomMiniHack-v0")

# Define the agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_custom_minihack")

# Test the trained agent
obs = env.reset()
done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()  # Optional: visualize the environment


num_episodes = 100
total_reward = 0

for episode in range(num_episodes):
    obs = env.reset()
    done = False
    episode_reward = 0
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        episode_reward += reward
    total_reward += episode_reward

print(f"Average reward over {num_episodes} episodes: {total_reward / num_episodes}")
