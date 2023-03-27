import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from tbx import basedir


def get_folder(prefix="cu_5.0_e_inpt_4387/train_n2_s1"):
    return basedir / f"{prefix}/oneoff_ipi_heat_1"


tasks = {
    "cu_5.0_e_inpt_4387/train_n2_s1": "cu5_n2",
    "../verdi/cu_5.0_1/train_n2_n1": "cu5_n2_verdi",
    "../verdi/cu_5.0_1/train_cont_n2_s1_n1": "cu5_n2_verdi_cont",
}

for task, name in tasks.items():
    raw = np.loadtxt(get_folder(task) / "simulation.out")

    time = raw[1:, 1]
    set_temp = raw[1:, 2]
    temp = raw[1:, 3]
    vol = raw[1:, 4] / 3**3

    time = xr.DataArray(time, name="time", dims=("time"))  # in ps
    temp = xr.DataArray(temp, coords={"time": time}, dims=("time"), name="temperature")
    set_temp = xr.DataArray(
        set_temp, coords={"time": time}, dims=("time"), name="external_temperature"
    )
    vol = xr.DataArray(vol, coords={"time": time}, dims=("time"), name="volume")

    dataset = xr.Dataset(
        {
            "temperature": temp,
            "external_temperature": set_temp,
            "volume": vol,
        }
    )

    dataset.to_netcdf(f"{name}.nc")

