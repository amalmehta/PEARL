"""Train one PEARL run.

    python -m pearl.train --env point --variant pearl --seed 0 --out runs/point/pearl/seed0
"""
import argparse
import json
import logging

import torch

from .config import BUDGET, PAPER_ENV, VARIANTS, make_config
from .trainer import PEARL


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--env", choices=list(PAPER_ENV), default="point")
    p.add_argument("--variant", choices=list(VARIANTS), default="pearl")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default=None)
    p.add_argument("--threads", type=int, default=2)
    p.add_argument("--paper-scale", action="store_true", help="ignore the laptop budget overrides")
    p.add_argument("--override", default="{}", help='JSON dict of config overrides, e.g. \'{"num_iterations": 2}\'')
    args = p.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    torch.set_num_threads(args.threads)
    cfg = make_config(args.env, args.variant, budget=not args.paper_scale, **json.loads(args.override))
    PEARL(cfg, seed=args.seed, out_dir=args.out).train()


if __name__ == "__main__":
    main()
