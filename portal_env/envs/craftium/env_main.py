from portal_env import EnvSidePortal
from portal_env.config import config
import gymnasium
import numpy as np
import craftium


class PortalWrapper(gymnasium.Wrapper):
    def __init__(self, env, *args, **kwargs):
        super().__init__(env)

    def step(self, action: np.ndarray):
        assert isinstance(action, np.ndarray), f"Got {action} instead"
        if action.ndim == 0:
            action = action.item()
        return self.env.step(action)
    

class HardResetCraftium(gymnasium.Env):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._args = args
        self._kwargs = kwargs
        self._env = gymnasium.make(*args, **kwargs)
        self.action_space = self._env.action_space
        self.observation_space = self._env.observation_space

    def reset(self, *, seed=None, options=None):
        self._env.close()
        self._env = gymnasium.make(*self._args, **self._kwargs)
        return self._env.reset(seed=seed, options=options)

    def step(self, action):
        return self._env.step(action)

    def close(self):
        return self._env.close()

    def render(self):
        return self._env.render()

    def __getattr__(self, name):
        return getattr(self._env, name)
    

def env_factory(*args, **kwargs):
    env = gymnasium.make(*args, **kwargs)
    return PortalWrapper(env)


def main():
    portal = EnvSidePortal(env_factory=env_factory, port=config.env_ports['craftium'])
    portal.start()


if __name__ == '__main__':
    main()
