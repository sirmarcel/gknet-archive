import numpy as np

from vibes.trajectory import reader
from pathlib import Path

from gknet import Data

from data_settings import *


data = Data(cutoff=cutoff, offset=offset)
traj = reader("/talos/scratch/mlang/gknet/raw/verdi/verdi.son")
data.add_atoms(traj, stress=True)
data.save(outdir / f"verdi_vasp.torch")

data = Data(cutoff=cutoff, offset=offset)
traj = reader("/talos/scratch/mlang/gknet/raw/verdi/aims.son")
data.add_atoms(traj, stress=True)
data.save(outdir / f"verdi_aims.torch")
