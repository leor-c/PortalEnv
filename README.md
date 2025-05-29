# Portal-Env

A tool for Reinforcement Learning that separates the runtime environment of agents and their environments 
(worlds/games). This package addresses the challenges of dependency management in RL development by using 
containerized environments for both agents and their worlds.


Portal-Env creates a clean separation between:
1. The **agent's runtime environment** - where the RL algorithm is implemented and executed.
2. The **environment's runtime environment** - containing the environment (e.g., game/world) and its dependencies.

This separation is implemented via a communication "portal" that enables seamless interaction between 
the agent and the environment while keeping their runtime environments isolated.

### Design Overview

#### 1. Agent Side  
- Runs the RL algorithm.
- Includes dependencies required for the agent's logic and training.
- Interfaces with the environment through an `AgentSidePortal`.

#### 2. Environment Side  
- Runs within an isolated container.
- Initializes and manages the RL environment.
- Includes environment-specific dependencies.
- Interfaces with the agent through an `EnvSidePortal`.


## Installation
### Requirements
- Docker

```bash
pip install portal-env
```


## Usage

### Basic Agent Usage

After starting the environment-side portal (detailed below), you can interact with the environment using 
the `AgentSidePortal`, which takes optional arguments for environment setup:
```python
from portal_env import AgentSidePortal
from stable_baselines3 import PPO


# Initialize the agent-side portal and the environment
env = AgentSidePortal("ALE/Pong-v5")  # pass environment setup arguments here

# Initialize the agent
agent = PPO("MlpPolicy", env, verbose=1)
agent.learn(total_timesteps=10000)
...

```
Or 
```python
from portal_env import AgentSidePortal
from my_agent import Agent


# Initialize the agent-side portal and the environment
env = AgentSidePortal("ALE/Pong-v5")  # pass environment setup arguments here

# Initialize the agent
agent = Agent(env.action_space)

# Run an episode
obs, info = env.reset()
done = False
while not done:
    action = agent.act(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
```


### Launching an Environment Portal
We provide a collection of pre-built environment portals for popular environments, 
together with a cli tool `portal-env` for launching them (and also custom environment portals).
Currently, we support the following environments:
- Atari Learning Environment (`ale`)
- Mujoco and Gymnasium environments (`mujoco`)

We hope to support more environments in the future.
Contributions are welcome!

To launch a supported environment using the cli tool, use:
```bash
portal-env start <env_name>
```
This command will start the environment portal by automatically building the Docker image and 
starting a corresponding Docker container.
As in the example above, environment setup arguments should be passed to the `AgentSidePortal` (agent-side).

#### Custom Environment Portals

To interact with a custom environment, you need to provide two files:

1. **Environment Main Script** (`env_main.py`):
A script that starts the environment-side portal (server) and provides it with an environment factory, a callable that creates and returns a new environment instance upon call.
```python
from portal_env import EnvSidePortal
from your_env import YourEnvironment  # Your custom environment

if __name__ == "__main__":
    portal = EnvSidePortal(env_factory=YourEnvironment)
    portal.run()
```

E.g., to set up an Atari environment portal:
```python
from portal_env import EnvSidePortal
import gymnasium
import ale_py


def main():
    portal = EnvSidePortal(env_factory=gymnasium.make)
    portal.start()


if __name__ == '__main__':
    main()
```
Note that the environment's dependencies (e.g., `ale_py`) should only be installed in the *environment* Dockerfile (see below).

2. **Environment Dockerfile** (`Dockerfile.env`):
A Dockerfile for building the Docker image of the environment. This Dockerfile should contain the following:
- Install environment-specific dependencies
- Install Portal-Env dependencies: `RUN pip install portal-env`
- Copy your environment code
- Run the main script from step 1 above using e.g., `CMD ["python", "env_main.py"]`.
```dockerfile
FROM python:3.12-slim

# Install environment-specific dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your environment code
COPY . .

# Run the environment portal
CMD ["python", "env_main.py"]
```


You can launch your custom environments automatically using the cli tool:
```bash
portal-env start -p <path-to-custom-env-dir> <custom-env-name>
```
where `<path-to-custom-env-dir>` is the path to the directory containing the `Dockerfile.env` and `env_main.py` files,
and `<custom-env-name>` is the name of the environment.



## License

MIT License 


## Credits
- [Portal](https://github.com/danijar/portal) (https://github.com/danijar/portal)
