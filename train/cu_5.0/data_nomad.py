import numpy as np

from vibes.trajectory import reader
from pathlib import Path

from gknet import Data

from data_settings import *


data = Data(cutoff=cutoff, offset=offset)
for temp in range(300, 2401, 300):
    for ens in [0, 1, 2]:
        traj = reader(f"/talos/scratch/mlang/gknet/cc/og/{temp}_{ens}.son")
        data.add_atoms(traj[::10], stress=False)

data.save(outdir / f"nomad.torch")
