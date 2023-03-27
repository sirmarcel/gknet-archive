import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

from vibes.phonopy.postprocess import postprocess
from vibes.phonopy.wrapper import set_bandstructure

basedir = Path(
    "/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1"
)
aimsdir = Path("../../../gknet-aims/")


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


# np.savez_compressed(
#     f"tetra_aims_n96.npz",
#     **get_phonons(aimsdir / f"new_cc_tetragonal/phonons/s2_k6_rho1e-7_cc_light/"),
# )
# np.savez_compressed(
#     f"tetra_aims_n96_tight.npz",
#     **get_phonons(aimsdir / f"new_cc_tetragonal/phonons/s2_k6_rho1e-7_tight/"),
# )
np.savez_compressed(
    f"tetra_aims_n324.npz",
    **get_phonons(
        aimsdir / f"new_cc_tetragonal/fk_phonons/s3/", suffix="trajectory.son"
    ),
)

np.savez_compressed(
    f"fk_tetra_aims_96.npz",
    **get_phonons(
        aimsdir / f"new_cc_tetragonal/phonons/fk_s2_k2_rho1e-7_cc_light/",
    ),
)

np.savez_compressed(
    f"fk_tetra_aims_324.npz",
    **get_phonons(
        aimsdir / f"new_cc_tetragonal/phonons/fk_s3_k2_rho1e-7_cc_light/",
    ),
)

np.savez_compressed(
    f"fk_tetra_aims_324_k4.npz",
    **get_phonons(
        aimsdir / f"new_cc_tetragonal/phonons/fk_s3_k4_rho1e-7_cc_light/",
    ),
)


np.savez_compressed(
    f"mono_aims_n96.npz",
    **get_phonons(aimsdir / f"new_verdi_monoclinic/phonons/s2_k6_rho1e-7_cc_light/"),
)
np.savez_compressed(
    f"mono_aims_n96_tight.npz",
    **get_phonons(aimsdir / f"new_verdi_monoclinic/phonons/s2_k6_rho1e-7_tight/"),
)
np.savez_compressed(
    f"mono_aims_n324.npz",
    **get_phonons(aimsdir / f"new_verdi_monoclinic/phonons/s3_k4_rho1e-7_cc_light/"),
)
np.savez_compressed(
    f"mono_aims_n768.npz",
    **get_phonons(aimsdir / f"new_verdi_monoclinic/phonons/s4_k2_rho1e-7_cc_light/"),
)


# for n in [96, 324]:
#     np.savez_compressed(
#         f"tetra_schnet_n{n}.npz",
#         **get_phonons(basedir / f"verdi_tetragonal/phonons_aims_n{n}/"),
#     )

#     np.savez_compressed(
#         f"tetra_aims_n{n}.npz",
#         **get_phonons(aimsdir / f"verdi_tetragonal/phonons_k2_n{n}/"),
#     )


# for n in [96, 324]:
#     np.savez_compressed(
#         f"mono_schnet_n{n}.npz",
#         **get_phonons(basedir / f"verdi_monoclinic/phonons_aims_n{n}/"),
#     )

#     np.savez_compressed(
#         f"mono_aims_n{n}.npz",
#         **get_phonons(aimsdir / f"verdi_monoclinic/phonons_k2_n{n}/"),
#     )
