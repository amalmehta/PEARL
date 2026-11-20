"""Per-task replay buffers (one ring buffer per task), as in oyster's MultiTaskReplayBuffer."""
import numpy as np


class TaskBuffer:
    def __init__(self, obs_dim, action_dim, capacity):
        self.capacity = capacity
        self.obs = np.zeros((capacity, obs_dim), np.float32)
        self.actions = np.zeros((capacity, action_dim), np.float32)
        self.rewards = np.zeros((capacity, 1), np.float32)
        self.sparse_rewards = np.zeros((capacity, 1), np.float32)
        self.next_obs = np.zeros((capacity, obs_dim), np.float32)
        self.terminals = np.zeros((capacity, 1), np.float32)
        self.clear()

    def clear(self):
        self.top = 0
        self.size = 0
        self.episode_starts = []

    def add_path(self, path):
        n = len(path["obs"])
        if self.size == self.capacity:
            # ring buffer wrapped: forget episodes whose start is about to be overwritten
            overwritten = {(self.top + i) % self.capacity for i in range(n)}
            self.episode_starts = [s for s in self.episode_starts if s not in overwritten]
        self.episode_starts.append(self.top)
        for i in range(n):
            t = self.top
            self.obs[t] = path["obs"][i]
            self.actions[t] = path["actions"][i]
            self.rewards[t] = path["rewards"][i]
            self.sparse_rewards[t] = path["sparse_rewards"][i]
            self.next_obs[t] = path["next_obs"][i]
            self.terminals[t] = path["terminals"][i]
            self.top = (self.top + 1) % self.capacity
            self.size = min(self.size + 1, self.capacity)

    FIELDS = ("obs", "actions", "rewards", "sparse_rewards", "next_obs", "terminals")

    def state(self):
        """Only the filled rows, so a checkpoint is small (for resuming a stopped run)."""
        return dict(top=self.top, size=self.size, episode_starts=list(self.episode_starts),
                    **{k: getattr(self, k)[: self.size].copy() for k in self.FIELDS})

    def load_state(self, s):
        self.top, self.size, self.episode_starts = s["top"], s["size"], list(s["episode_starts"])
        for k in self.FIELDS:
            getattr(self, k)[: self.size] = s[k]

    def _take(self, idx):
        return {
            "obs": self.obs[idx], "actions": self.actions[idx], "rewards": self.rewards[idx],
            "sparse_rewards": self.sparse_rewards[idx], "next_obs": self.next_obs[idx],
            "terminals": self.terminals[idx],
        }

    def random_batch(self, n, rng):
        return self._take(rng.integers(0, self.size, n))

    def random_sequence(self, n, rng):
        """Whole trajectories in order, concatenated and cut to n (oyster's random_sequence)."""
        starts = sorted(self.episode_starts)
        idx = []
        while len(idx) < n:
            k = rng.integers(0, len(starts))
            end = starts[k + 1] if k + 1 < len(starts) else self.size
            idx.extend(range(starts[k], end))
        return self._take(np.asarray(idx[:n]))


class MultiTaskBuffer:
    def __init__(self, n_tasks, obs_dim, action_dim, capacity):
        self.tasks = [TaskBuffer(obs_dim, action_dim, capacity) for _ in range(n_tasks)]

    def __getitem__(self, idx):
        return self.tasks[idx]

    def state(self):
        return [t.state() for t in self.tasks]

    def load_state(self, states):
        for t, s in zip(self.tasks, states):
            t.load_state(s)
