import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

from vibes.phonopy.postprocess import postprocess
from vibes.phonopy.wrapper import set_bandstructure


def get_dir(cutoff=5.0, t=2):
    return Path(
        f"/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_{cutoff:.1f}_e_inpt_4387/train_n{t}_s1"
    )


def get_phonons(folder, suffix="phonopy/trajectory.son"):
    phonons = postprocess(folder / suffix, enforce_sum_rules=False)

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


for cutoff in [4.0, 5.0, 6.0]:
    for t in [1, 2]:
        np.savez_compressed(
            f"tetra_schnet_{cutoff:.1f}_n{t}_n96.npz",
            **get_phonons(get_dir(cutoff, t) / f"new_phonons/tetragonal/phonons_s2/"),
        )

        np.savez_compressed(
            f"mono_schnet_{cutoff:.1f}_n{t}_n96.npz",
            **get_phonons(get_dir(cutoff, t) / f"new_phonons/monoclinic/phonons_s2/"),
        )

        np.savez_compressed(
            f"tetra_schnet_{cutoff:.1f}_n{t}_n324.npz",
            **get_phonons(get_dir(cutoff, t) / f"new_phonons/tetragonal/phonons_s3/"),
        )

        np.savez_compressed(
            f"mono_schnet_{cutoff:.1f}_n{t}_n324.npz",
            **get_phonons(get_dir(cutoff, t) / f"new_phonons/monoclinic/phonons_s3/"),
        )
