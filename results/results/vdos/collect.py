import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

# from vibes.green_kubo.velocities import get_vdos as vibes_get_vdos


basedir = Path("/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/")
reference = Path("/talos/scratch/mlang/gknet/cc_rerun")
maxfreq = 30
npad = 10000
window = 25


def vibes_get_vdos(
    velocities, masses, hann=False, npad=10000
):
    # borrowed from https://gitlab.com/vibes-developers/vibes/-/merge_requests/57/
    from vibes.correlation import get_autocorrelationNd
    from vibes.fourier import get_fourier_transformed

    n_atoms = velocities.shape[1]

    assert len(masses) == n_atoms, (len(masses), n_atoms)

    # mass-scale the velocities
    velocities *= masses[None, :, None] ** 0.5

    v_corr = get_autocorrelationNd(velocities, normalize=True, hann=hann)
    df_vdos = get_fourier_transformed(v_corr, npad=npad)

    return df_vdos


def get_reference(temperature, ens):
    return xr.open_mfdataset(str(reference / f"{temperature}_{ens}/*.nc"))


def get_rerun(folder, temperature, ens):
    return xr.open_mfdataset(
        str(Path(folder) / f"{temperature}/{ens}/md/trajectory/*.nc")
    )


def get_single_vdos(dataset):
    velocities = dataset.velocities.compute()
    masses = dataset.masses
    vdos = vibes_get_vdos(velocities=velocities, masses=masses, hann=False, npad=npad)
    df = vdos.real.sum(axis=(1, 2)).to_series()[:maxfreq].rolling(window=window).mean()
    return df.to_xarray()


def get_combined_vdos(datasets):
    datasets = xr.concat([get_single_vdos(d) for d in datasets], dim="trajectory")
    return datasets


experiments = {
    "default": basedir / "e_inpt_4387/train_1_5/cc_rerun",
    "cu7.0_n5": basedir / "cu_7.0_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu7.0_n1": basedir / "cu_7.0_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu6.5_n5": basedir / "cu_6.5_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu6.5_n1": basedir / "cu_6.5_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu6.0_n5": basedir / "cu_6.0_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu6.0_n1": basedir / "cu_6.0_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu5.5_n5": basedir / "cu_5.5_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu5.5_n1": basedir / "cu_5.5_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu5.0_n5": basedir / "cu_5.0_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu5.0_n2": basedir / "cu_5.0_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu5.0_n2_fnl": basedir / "cu_5.0_e_inpt_4387/train_n2_s1/fixed_nl_cc_rerun",
    "cu5.0_n1": basedir / "cu_5.0_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu5.0_n1_fnl": basedir / "cu_5.0_e_inpt_4387/train_n1_s1/fixed_nl_cc_rerun",
    "cu4.5_n5": basedir / "cu_4.5_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu4.5_n1": basedir / "cu_4.5_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu4.0_n5": basedir / "cu_4.0_e_inpt_4387/train_n5_s1/cc_rerun",
    "cu4.0_n1": basedir / "cu_4.0_e_inpt_4387/train_n1_s1/cc_rerun",
    "cu7.0_n2": basedir / "cu_7.0_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu6.5_n2": basedir / "cu_6.5_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu6.0_n2": basedir / "cu_6.0_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu5.5_n2": basedir / "cu_5.5_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu5.0_n2": basedir / "cu_5.0_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu4.5_n2": basedir / "cu_4.5_e_inpt_4387/train_n2_s1/cc_rerun",
    "cu4.0_n2": basedir / "cu_4.0_e_inpt_4387/train_n2_s1/cc_rerun",
}


results_300 = {
    k: get_combined_vdos([get_rerun(v, 300, i) for i in range(3)])
    for k, v in experiments.items()
}

results_300["aims"] = get_combined_vdos([get_reference(300, i) for i in range(3)])

results_300 = xr.Dataset(results_300)

results_300.to_netcdf("result_300.nc")
