import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

from vibes.phonopy.postprocess import postprocess
from vibes.phonopy.wrapper import set_bandstructure

basedir = Path("/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1")
aimsdir = Path("/talos/scratch/mlang/gknet-aims")

def get_phonons(folder):
    phonons = postprocess(
        folder / "phonopy/trajectory.son", enforce_sum_rules=False
    )

    set_bandstructure(phonons)

    q_mesh = [45, 45, 45]
    phonons.run_mesh(q_mesh)
    phonons.run_total_dos(use_tetrahedron_method=True)

    return {
        "bs_all_distances": np.array(phonons._band_structure._distances),
        "bs_all_frequencies": np.array(phonons._band_structure._frequencies),
        "bs_labels": np.array(phonons._band_structure._labels),
        "bs_special_points": np.array(phonons._band_structure._special_points),
        "dos_frequency_points": np.array(phonons._total_dos._frequency_points),
        "dos_total_dos": np.array(phonons._total_dos._dos),
    }

for n in [96, 324]:
    np.savez_compressed(
        f"tetra_schnet_n{n}.npz",
        **get_phonons(basedir / f"verdi_tetragonal/phonons_aims_n{n}/"),
    )

    np.savez_compressed(
        f"tetra_aims_n{n}.npz",
        **get_phonons(aimsdir / f"verdi_tetragonal/phonons_k2_n{n}/"),
    )


for n in [96, 324]:
    np.savez_compressed(
        f"mono_schnet_n{n}.npz",
        **get_phonons(basedir / f"verdi_monoclinic/phonons_aims_n{n}/"),
    )

    np.savez_compressed(
        f"mono_aims_n{n}.npz",
        **get_phonons(aimsdir / f"verdi_monoclinic/phonons_k2_n{n}/"),
    )


