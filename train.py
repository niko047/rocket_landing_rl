import gymnasium as gym
from stable_baselines3 import PPO
from rocket_env import RocketLandingEnv

# Register the environment
gym.register(
    id='RocketLanding-v0',
    entry_point='rocket_env:RocketLandingEnv',
)

# Create environment
env = gym.make('RocketLanding-v0')

# Initialize the agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=1000000)

# Save the trained model
model.save("rocket_landing_ppo")

# Test the trained agent
obs, _ = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    if done or truncated:
        obs, _ = env.reset() 