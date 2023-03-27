import numpy as np

from vibes.trajectory import reader
from pathlib import Path

from gknet import Data

from data_settings import *


for temp in [300, 2400]:
    data = Data(cutoff=cutoff, offset=offset)
    for ens in [0, 1, 2]:
        traj = reader(f"/talos/scratch/mlang/gknet/cc_rerun/{temp}_{ens}.son")
        data.add_atoms(traj, stress=True)
    data.save(outdir / f"cc_rerun_{temp}.torch")


for temp in [300, 1500, 2400]:
    data = Data(cutoff=cutoff, offset=offset)
    for ens in [0, 1, 2]:
        traj = reader(f"/talos/scratch/mlang/gknet/cc/re5/{temp}_{ens}.son")
        data.add_atoms(traj, stress=True)
    data.save(outdir / f"cc_re5_{temp}.torch")
