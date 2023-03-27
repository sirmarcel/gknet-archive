"""Green-Kubo post processing"""
from collections import namedtuple

import numpy as np
import xarray as xr
from ase import units
from scipy import signal as sl

from vibes import defaults
from vibes import dimensions as dims
from vibes import keys
from vibes.correlation import get_autocorrelationNd
from vibes.fourier import get_fourier_transformed
from vibes.helpers import Timer, talk, warn
from vibes.helpers.filter import get_filtered
from vibes.integrate import get_cumtrapz

from vibes.green_kubo import get_gk_prefactor_from_dataset, get_lowest_vibrational_frequency, get_hf_data

from stepson.comms import Comms

comms = Comms("greenkubo")


_prefix = "GreenKubo"

Timer.prefix = _prefix


def _talk(msg, **kw):
    """wrapper for `utils.talk` with prefix"""
    return talk(msg, prefix=_prefix, **kw)


def get_gk_dataset(
    dataset: xr.Dataset,
    window_factor: int = defaults.window_factor,
    filter_prominence: float = defaults.filter_prominence,
    discard: int = 0,
    total: bool = False,
    verbose: bool = True,
) -> xr.Dataset:
    """get Green-Kubo data from trajectory dataset

    Args:
        dataset: a dataset containing `heat_flux` and describing attributes
        window_factor: factor for filter width estimated from VDOS (default: 1)
        filter_prominence: prominence for peak detection
        discard: discard this many timesteps from the beginning of the trajectory
        total: postprocess gauge-invariant terms of heat flux as well

    Returns:
        xr.Dataset: the processed data

    Workflow:
        1. get heat flux autocorrelation function (HFACF) and the integrated kappa
        2. get lowest significant vibrational frequency and get its time period
        3. filter integrated kappa with this period
        4. get HFACF by time derivative of this filtered kappa
        5. filter the HFACF with the same filter
        6. estimate cutoff time from the decay of the filtered HFACF

    """
    reporter = comms.reporter()
    reporter.start("getting green-kubo dataset")
    reporter.step("get hf")
    # 1. get HFACF and integrated kappa
    heat_flux = dataset[keys.heat_flux]

    if total:  # add non-gauge-invariant contribution
        heat_flux += dataset[keys.heat_flux_aux]

    reporter.step("get hfacf")
    hfacf, kappa = get_hf_data(heat_flux)

    # convert to W/mK
    reporter.step("get prefactor", spin=False)
    pref = get_gk_prefactor_from_dataset(dataset, verbose=verbose)
    hfacf *= pref
    kappa *= pref

    # 2. get lowest significant frequency (from VDOS) in THz
    reporter.step("get vibrational frequency")
    kw = {"prominence": filter_prominence}
    freq = get_lowest_vibrational_frequency(dataset[keys.velocities], **kw)

    if abs(freq) < 0.001:
        comms.warn(f"Lowest significant vib. freq is {freq} THz, CHECK VDOS!", level=2)

    # window in fs from freq.:
    window_fs = window_factor / freq * 1000

    comms.talk(f"Estimate filter window size")
    comms.talk(f".. lowest vibrational frequency: {freq:.4f} THz")
    comms.talk(f".. corresponding window size:    {window_fs:.4f} fs")
    comms.talk(f".. window multiplicator used:    {window_factor:.4f} fs")

    # 3. filter integrated HFACF (kappa) with this window respecting antisymmetry in time
    reporter.step("filter integrated hfacf", spin=False)
    kw = {"window_fs": window_fs, "antisymmetric": True, "verbose": verbose}
    k_filtered = get_filtered(kappa, **kw)

    # 4. get the respective HFACF by differentiating w.r.t. time and filtering again
    reporter.step("get filtered hfacf")
    k_gradient = kappa.copy()

    # compute derivative with j = dk/dt = dk/dn * dn/dt = dk/dn / dt
    dt = float(kappa.time[1] - kappa.time[0])
    k_gradient.data = np.gradient(k_filtered, axis=0) / dt

    j_filtered = get_filtered(k_gradient, window_fs=window_fs, verbose=False)

    # 5. get cutoff times from j_filtered and save respective kappas
    reporter.step("get cutoff times")
    ts = np.zeros([3, 3])
    ks = np.zeros([3, 3])

    for (ii, jj) in np.ndindex(3, 3):
        j = j_filtered[:, ii, jj]
        times = j.time[j < 0]
        if len(times) > 1:
            ta = times.min()
        else:
            comms.warn(f"no cutoff time found")
            ta = 0
        ks[ii, jj] = k_filtered[:, ii, jj].sel(time=ta)
        ts[ii, jj] = ta

    # report
    if verbose:
        k_diag = np.diag(ks)
        for msg in ["Cutoff times (fs):", *np.array2string(ts, precision=3).split("\n")]:
            comms.talk(msg)
        comms.talk(f"Kappa is:       {np.mean(k_diag):.3f} +/- {np.std(k_diag) / 3**.5:.3f}")
        for msg in ["Kappa^ab is: ", *np.array2string(ks, precision=3).split("\n")]:
            comms.talk(msg)

    # 6. compile new dataset
    reporter.step("make dataset")
    attrs = dataset.attrs.copy()
    attrs.update({"gk_window_fs": window_fs})

    _filtered = "_filtered"
    data = {
        keys.hf_acf: hfacf,
        keys.hf_acf + _filtered: j_filtered,
        keys.kappa_cumulative: kappa,
        keys.kappa_cumulative + _filtered: k_filtered,
        keys.kappa: (dims.tensor, ks),
        keys.time_cutoff: (dims.tensor, ts),
    }

    data = xr.Dataset(data, coords=kappa.coords, attrs=attrs)

    reporter.done()
    return data
