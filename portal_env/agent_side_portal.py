import portal
import numpy as np
from typing import Any
import gymnasium as gym
from portal_env.config import config
from portal_env.utils import parse_gym_space


class AgentSidePortal(gym.Env):
    def __init__(self, *env_args, **env_kwargs):
        self.portal = portal.Client(f"{config.host_name}_ale:{config.port}")
        self._env_id = None

        self._init_env(*env_args, **env_kwargs)

    def _init_env(self, *args, **kwargs):
        assert self._env_id is None, "Environment already initialized"
        future = self.portal.create(*args, **kwargs)
        self._env_id = future.result()

    def _assert_env_init(self):
        assert self._env_id is not None, "Environment not initialized"

    def reset(self, **kwargs) -> tuple[np.ndarray, dict[str, Any]]:
        self._assert_env_init()
        future = self.portal.reset(self._env_id)
        return future.result()

    def step(self, action) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        self._assert_env_init()
        future = self.portal.step(self._env_id, action)
        return future.result()

    @property
    def action_space(self):
        self._assert_env_init()
        future = self.portal.action_space(self._env_id)
        return parse_gym_space(future.result())

    @property
    def observation_space(self):
        self._assert_env_init()
        future = self.portal.observation_space(self._env_id)
        return parse_gym_space(future.result())


