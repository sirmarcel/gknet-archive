import xarray as xr
import numpy as np
from pathlib import Path
from ase.constraints import voigt_6_to_full_3x3_stress

from stepson.comms import comms
from stepson.trajectory.dataset import Trajectory
from stepson.trajectory.step import normalize_stress

from vibes import keys, dimensions


results_keys = {
    "forces": keys.forces,
    "energy": keys.energy_potential,
    "stress": keys.stress_potential,
    "stresses": keys.stresses_potential,
    keys.virials: keys.virials,
    "energies": "energies_potential",
    "barycenter_r0_heat_flux": "barycenter_r0_heat_flux",
    "barycenter_r0_heat_flux_pot": "barycenter_r0_heat_flux_pot",
    "barycenter_r0_heat_flux_kin": "barycenter_r0_heat_flux_kin",
    "barycenter_rt_heat_flux": "barycenter_rt_heat_flux",
    "barycenter_rt_heat_flux_pot": "barycenter_rt_heat_flux_pot",
    "barycenter_rt_heat_flux_kin": "barycenter_rt_heat_flux_kin",
    "fan_virials": "fan_virials",
    "fan_virials_mpnn": "fan_virials_mpnn",
    "fan_virials_transpose": "fan_virials_transpose",
    "fan_virials_symm": "fan_virials_symm",
    "heat_flux": "heat_flux",
    "heat_flux_force_term": "heat_flux_force_term",
    "heat_flux_potential_term": "heat_flux_potential_term",
}

keys_and_dims = {
    keys.forces: dimensions.time_atom_vec,
    keys.energy_potential: dimensions.time,
    keys.stress_potential: dimensions.time_tensor,
    keys.stresses_potential: dimensions.time_atom_tensor,
    keys.virials: dimensions.time_atom_tensor,
    "energies_potential": dimensions.time_atom,
    "barycenter_r0_heat_flux": dimensions.time_vec,
    "barycenter_r0_heat_flux_pot": dimensions.time_vec,
    "barycenter_r0_heat_flux_kin": dimensions.time_vec,
    "barycenter_rt_heat_flux": dimensions.time_vec,
    "barycenter_rt_heat_flux_pot": dimensions.time_vec,
    "barycenter_rt_heat_flux_kin": dimensions.time_vec,
    "fan_virials": dimensions.time_atom_tensor,
    "fan_virials_mpnn": dimensions.time_atom_tensor,
    "fan_virials_transpose": dimensions.time_atom_tensor,
    "fan_virials_symm": dimensions.time_atom_tensor,
    "heat_flux": dimensions.time_vec,
    "heat_flux_force_term": dimensions.time_vec,
    "heat_flux_potential_term": dimensions.time_vec,
}


class Recompute:
    def __init__(
        self,
        infolder,
        outfolder,
        calculator,
        batch_size=100,
        batched=False,
        step=1,
        stop=None,
    ):
        self.infolder = Path(infolder)
        self.outfolder = Path(outfolder)
        self.calculator = calculator
        self.batch_size = batch_size
        self.step = step
        self.external_stop = stop

        comms.talk(f"recomputing {self.infolder}", full=True)
        comms.talk(f"writing to {self.outfolder}", full=True)
        if self.step != 1:
            comms.talk(f"computing every {self.step}-th step", full=True)

        if self.external_stop is not None:
            comms.talk(f"computing up to {self.external_stop}-th step", full=True)

        self.metadata = {"infolder": str(self.infolder)}

        self.reporter = comms.reporter()

        self.batched = batched  # use batched calculator
        if self.batched:
            comms.talk("computing whole batches")

    def prepare(self):
        self.reporter.start("recomputing")

        self.reporter.step("prepare/restore")
        self.trajectory = Trajectory(self.infolder)

        if self.external_stop is None:
            self.stop = len(self.trajectory)
        else:
            self.stop = self.external_stop

        idx = 0
        idx_chunk = 0
        if self.outfolder.is_dir():
            outfiles = list(self.outfolder.glob("*.nc"))
            if len(outfiles) > 0:
                idx_chunk = len(outfiles)
                idx = len(xr.open_mfdataset(outfiles).time) * self.step
                comms.talk(f"restarting from step {idx}, chunk {idx_chunk}")
        else:
            self.outfolder.mkdir(parents=True)

        self.idx = idx
        self.idx_chunk = idx_chunk

    def run(self, watchdog):
        self.prepare()

        self.reporter.step("calculating", spin=False)

        if self.batched:
            return self.run_batched(watchdog)
        else:
            return self.run_each_step(watchdog)

    def run_each_step(self, watchdog):
        chunk = {}
        while self.idx < self.stop:
            self.reporter.tick(f"step {self.idx}, chunk {self.idx_chunk}")

            t, atoms = self.trajectory.get_time_and_atoms(self.idx)
            self.calculator.calculate(atoms)
            results = self.calculator.results.copy()
            results2chunk(t, chunk, results)

            if (
                len(chunk["time"]) == self.batch_size
                or self.idx + self.step >= (self.stop)
                or watchdog()
            ):
                self.reporter.tick(f"write chunk {self.idx_chunk}")

                self.write(chunk)
                chunk = {}
                self.idx_chunk += 1

                if watchdog():
                    self.reporter.done()
                    comms.talk("stopped due to watchdog")
                    return False

            self.idx += self.step

        self.reporter.done()
        comms.talk("stopped normally")
        return True

    def run_batched(self, watchdog):
        while self.idx < self.stop:
            self.reporter.tick(f"step {self.idx}, chunk {self.idx_chunk}")
            end_batch = min(self.idx + self.step * self.batch_size, self.stop)
            time_and_atoms = [
                self.trajectory.get_time_and_atoms(idx)
                for idx in range(self.idx, end_batch, self.step)
            ]
            times, atomss = zip(*time_and_atoms)
            results = self.calculator.calculate(atomss)
            chunk = {}
            for key, value in results.items():
                if key in results_keys:
                    chunk[results_keys[key]] = np.array(value)
            chunk["time"] = np.array(times)
            if keys.stress_potential in chunk:
                chunk[keys.stress_potential] = voigt_6_to_full_3x3_stress(
                    chunk[keys.stress_potential]
                )

            self.reporter.tick(f"write chunk {self.idx_chunk}")
            self.write(chunk)

            self.idx_chunk += 1
            self.idx = end_batch

            if watchdog():
                self.reporter.done()
                comms.talk("stopped due to watchdog")
                return False

        self.reporter.done()
        comms.talk("stopped normally")
        return True

    def write(self, chunk):
        time = {"time": chunk.pop("time")}

        data = {}
        for key, value in chunk.items():
            data[key] = xr.DataArray(
                np.array(value), dims=keys_and_dims[key], coords=time, name=key
            )

        data = xr.Dataset(data, attrs=self.metadata, coords=time)

        data.to_netcdf(self.outfolder / f"recomputed_{self.idx_chunk:05d}.nc")


def results2chunk(t, chunk, results):
    data = {}
    for results_key, data_key in results_keys.items():
        if results_key in results:
            data[data_key] = results[results_key]

    if chunk == {}:
        chunk["time"] = []
        for key in data.keys():
            chunk[key] = []

    if keys.stress_potential in data:
        normalize_stress(data)

    if keys.stresses_potential in data:
        normalize_stresses(data)

    for key, value in data.items():
        chunk[key].append(value)

    chunk["time"].append(t)


def normalize_stresses(data):
    stresses = data[keys.stresses_potential]

    if stresses.shape[1:] == (6,):
        data[keys.stresses_potential] = voigt_6_to_full_3x3_stress(stresses)
