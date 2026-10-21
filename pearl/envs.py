"""2D task families for PEARL.

Point-Robot and Sparse Point-Robot follow oyster's rlkit/envs/point_robot.py exactly,
including the seed-1337 task lists, so task i here is task i there. Point-Wind is NOT in
the paper: it is a dynamics-varying family invented for this project.

The policy acts in [-1, 1]^2. Like oyster's NormalizedBoxEnv wrapper, `step` rescales the
action to the env's real bounds of [-0.1, 0.1]^2.
"""
import numpy as np

ACTION_SCALE = 0.1


class PointRobot:
    """Point on a plane, position control; task = goal in the unit square; reward = -distance."""

    name = "point"
    obs_dim = 2
    action_dim = 2
    horizon = 20
    sparse = False
    # dynamics are identical across tasks, so next_obs carries no task information
    use_next_obs_in_context = False

    def __init__(self, n_tasks=100):
        rs = np.random.RandomState(1337)  # same stream as oyster's np.random.seed(1337)
        self.tasks = [np.array([rs.uniform(-1.0, 1.0), rs.uniform(-1.0, 1.0)]) for _ in range(n_tasks)]
        self.rng = np.random.default_rng(0)
        self.reset_task(0)

    def seed(self, seed):
        self.rng = np.random.default_rng(seed)

    def reset_task(self, idx):
        self.task_idx = idx
        self.goal = self.tasks[idx]
        return self.reset()

    def reset(self):
        self.state = self.rng.uniform(-1.0, 1.0, size=2)
        return self.state.copy()

    def _move(self, action):
        self.state = self.state + ACTION_SCALE * np.clip(action, -1.0, 1.0)

    def step(self, action):
        self._move(action)
        reward = -float(np.linalg.norm(self.state - self.goal))
        return self.state.copy(), reward, False, {}


class SparsePointRobot(PointRobot):
    """Goals on a radius-1 half circle; reward only inside radius 0.2 of the goal (paper Fig. 7).

    `step` returns the dense reward and puts the sparse one in info, like oyster. The trainer
    decides which reward each consumer sees (see `context_reward`).
    """

    name = "sparse_point"
    sparse = True
    goal_radius = 0.2

    def __init__(self, n_tasks=100):
        super().__init__(n_tasks)
        rs = np.random.RandomState(1337)
        angles = np.linspace(0, np.pi, num=n_tasks)
        goals = np.stack([np.cos(angles), np.sin(angles)], axis=1)
        rs.shuffle(goals)
        self.tasks = [g for g in goals]
        self.reset_task(0)

    def reset(self):
        self.state = np.zeros(2)
        return self.state.copy()

    def sparsify(self, dense_reward):
        # oyster: r * (r >= -radius), then +1 inside the radius, i.e. 1 - distance inside, 0 outside
        return 1.0 + dense_reward if dense_reward >= -self.goal_radius else 0.0

    def step(self, action):
        obs, reward, done, info = super().step(action)
        info["sparse_reward"] = self.sparsify(reward)
        return obs, reward, done, info


class PointWind(PointRobot):
    """INVENTED for this project (not in the paper): the dynamics vary, the reward does not.

    Fixed goal at the origin; each task has a constant wind w ~ U[-0.08, 0.08]^2 added to
    every step. The observation is only the position, so the policy can't see the wind
    except through context. next_obs goes in the context, as the oyster docs advise
    for dynamics changes.
    """

    name = "point_wind"
    use_next_obs_in_context = True
    wind_max = 0.08

    def __init__(self, n_tasks=100):
        super().__init__(n_tasks)
        rs = np.random.RandomState(1337)
        self.tasks = [rs.uniform(-self.wind_max, self.wind_max, size=2) for _ in range(n_tasks)]
        self.reset_task(0)

    def reset_task(self, idx):
        self.task_idx = idx
        self.wind = self.tasks[idx]
        self.goal = np.zeros(2)
        return self.reset()

    def _move(self, action):
        self.state = self.state + ACTION_SCALE * np.clip(action, -1.0, 1.0) + self.wind


ENVS = {cls.name: cls for cls in (PointRobot, SparsePointRobot, PointWind)}


def make_env(name, n_tasks=100):
    return ENVS[name](n_tasks=n_tasks)
