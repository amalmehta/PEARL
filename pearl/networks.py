"""Networks: MLP critics, tanh-Gaussian policy, context encoders.

Initialisation follows rlkit: hidden weights use fanin_init (rlkit takes size[0], which for
a torch Linear weight is the *output* width, and we keep that quirk), hidden biases are 0.1,
and the last layer is U(-3e-3, 3e-3).
"""
import math

import torch
from torch import nn
from torch.distributions import Normal

LOG_STD_MIN, LOG_STD_MAX = -20.0, 2.0


def _fanin_init(linear):
    bound = 1.0 / math.sqrt(linear.weight.shape[0])
    nn.init.uniform_(linear.weight, -bound, bound)
    nn.init.constant_(linear.bias, 0.1)


def _last_init(linear, w=3e-3):
    nn.init.uniform_(linear.weight, -w, w)
    nn.init.uniform_(linear.bias, -w, w)


class MLP(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super().__init__()
        sizes = [input_size, *hidden_sizes]
        self.fcs = nn.ModuleList(nn.Linear(a, b) for a, b in zip(sizes[:-1], sizes[1:]))
        for fc in self.fcs:
            _fanin_init(fc)
        self.last_fc = nn.Linear(sizes[-1], output_size)
        _last_init(self.last_fc)

    def hidden(self, x):
        for fc in self.fcs:
            x = torch.relu(fc(x))
        return x

    def forward(self, *inputs):
        return self.last_fc(self.hidden(torch.cat(inputs, dim=-1)))


class TanhGaussianPolicy(MLP):
    """pi(a | s, z): Gaussian squashed by tanh. Outputs mean and log-std heads."""

    def __init__(self, input_size, hidden_sizes, action_dim):
        super().__init__(input_size, hidden_sizes, action_dim)
        self.last_fc_log_std = nn.Linear(hidden_sizes[-1], action_dim)
        _last_init(self.last_fc_log_std)

    def forward(self, x, deterministic=False):
        h = self.hidden(x)
        mean = self.last_fc(h)
        log_std = self.last_fc_log_std(h).clamp(LOG_STD_MIN, LOG_STD_MAX)
        std = log_std.exp()
        pre_tanh = mean if deterministic else mean + std * torch.randn_like(mean)
        action = torch.tanh(pre_tanh)
        # change of variables for tanh, with rlkit's epsilon
        log_prob = Normal(mean, std).log_prob(pre_tanh) - torch.log(1 - action.pow(2) + 1e-6)
        return action, mean, log_std, log_prob.sum(-1, keepdim=True)


class MlpEncoder(MLP):
    """Permutation-invariant encoder: each transition c_n -> factor params, independently."""

    recurrent = False

    def forward(self, context):  # (tasks, n, feat) -> (tasks, n, out)
        return super().forward(context)


class RecurrentEncoder(nn.Module):
    """MLP embedding -> LSTM over the context sequence -> params from the last hidden state."""

    recurrent = True

    def __init__(self, input_size, hidden_sizes, output_size):
        super().__init__()
        self.embed = MLP(input_size, hidden_sizes[:-1], hidden_sizes[-1])
        self.lstm = nn.LSTM(hidden_sizes[-1], hidden_sizes[-1], batch_first=True)
        self.last_fc = nn.Linear(hidden_sizes[-1], output_size)
        _last_init(self.last_fc)

    def forward(self, context):  # (tasks, n, feat) -> (tasks, 1, out)
        h = torch.relu(self.embed(context))
        out, _ = self.lstm(h)  # fresh zero state each call (see SYSTEM-DESIGN: deviations)
        return self.last_fc(out[:, -1:, :])
