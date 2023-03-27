import numpy as np

from vibes.trajectory import reader
from pathlib import Path

from gknet import Data

from data_settings import *

traj1 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_4.son")
traj2 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_3.son")
traj3 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_8.son")
traj4 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_7.son")

train = Data(cutoff=cutoff, offset=offset)
train.add_atoms(traj1[0:2000], stress=True)
train.add_atoms(traj2[0:2000], stress=True)
train.add_atoms(traj3[0:2000], stress=True)
train.add_atoms(traj4[0:2000], stress=True)
train.save(outdir / "train.torch")

valid = Data(cutoff=cutoff, offset=offset)
valid.add_atoms(traj1[2000:], stress=True)
valid.add_atoms(traj2[2000:], stress=True)
valid.add_atoms(traj3[2000:], stress=True)
valid.add_atoms(traj4[2000:], stress=True)
valid.save(outdir / "valid.torch")
