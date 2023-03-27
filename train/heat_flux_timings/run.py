import numpy as np
import yaml

from time import monotonic
from stepson.trajectory.dataset import Trajectory

from gknet.experimental.unfolded_heatflux import UnfoldedHeatFluxCalculator, Unfolder
from gknet.experimental import fastCalculator
from gknet.experimental.fast_calculator.converter import Converter

skin = 0.0
steps = 10
sizes = [96, 324, 768, 1500, 2592, 4116, 8748]
cutoff = 5.0
interactions = 2
model = f"/u/mlang/gknet/gknet/experiments/ccl_zro_t96/cu_{cutoff:.1f}_e_inpt_4387/train_n{interactions}_s1/train/best_model.torch"
device = "cuda:1"
verbose = False


def get_calculators():
    # need to be able to re-create for different sizes
    calc_unfolded = UnfoldedHeatFluxCalculator(
        model,
        verbose=verbose,
        skin=skin,
        skin_unfolder=skin,
        device=device,
        report_update=True,
        never_update=True,
    )

    calc_virials = fastCalculator(
        model,
        skin=skin,
        virials=True,
        hardy=False,
        transpose_derivatives=True,
        verbose=verbose,
        device=device,
        report_update=True,
        never_update=True,
    )

    calc_hardy = fastCalculator(
        model,
        skin=skin,
        virials=True,
        hardy=True,
        verbose=verbose,
        device=device,
        report_update=True,
        never_update=True,
    )

    calc_forces = fastCalculator(
        model,
        skin=skin,
        stress=True,
        virials=False,
        hardy=False,
        verbose=verbose,
        device=device,
        report_update=True,
        never_update=True,
    )

    return {"unfolded": calc_unfolded, "hardy": calc_hardy, "virials": calc_virials, "no_hf": calc_forces}


def run_timing(callable, trajectory):
    times = []
    for i in range(1, steps + 1):
        atoms = trajectory.get_atoms(i)

        start = monotonic()
        callable(atoms)
        times.append(monotonic() - start)

    return times


def get_trajectory(n):
    return Trajectory(
        f"/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n1_s1/fast_prod_1/300/n_{n}/00/md/trajectory"
    )


def warmup_calculators(calculators, trajectory):
    atoms = trajectory.get_atoms(0)

    for calculator in calculators.values():
        calculator.calculate(atoms)


def time_calculators(calculator, trajectory):
    return run_timing(calculator.calculate, trajectory)


def time_converter(trajectory):
    converter = Converter(cutoff + skin, skin=0, device=device)
    return run_timing(converter, trajectory)


def time_unfolder(trajectory):
    unfolder = Unfolder(cutoff * interactions + skin, skin=0)
    return run_timing(unfolder, trajectory)


def time_unfolder_and_converter(trajectory):
    unfolder = Unfolder(cutoff * interactions + skin, skin=0)
    converter = Converter(cutoff + skin, skin=0, device=device)

    def both(atoms):
        unfolded = unfolder(atoms).atoms
        converter(unfolded)

    return run_timing(both, trajectory)


def process_times(times):
    return {"times": times, "mean": np.mean(times), "stddev": np.std(times)}


print("getting unfolded sizes")
unfolded_sizes = {}
unfolder = Unfolder(cutoff * interactions + skin, skin=0)
for n in sizes:
    trajectory = get_trajectory(n)
    atoms = trajectory.get_atoms(0)
    unfolded = unfolder(atoms).atoms
    unfolded_sizes[n] = len(unfolded)
    print(f"n={n}: {unfolded_sizes[n]}")

with open("sizes.yaml", "w") as f:
    yaml.dump(unfolded_sizes, f)


results = {}
for n in sizes:
    results[n] = {}
    calculators = get_calculators()

    print(f"working on n={n}")
    trajectory = get_trajectory(n)

    print("... timing converters")
    results[n]["convert"] = process_times(time_converter(trajectory))
    results[n]["unfold"] = process_times(time_unfolder(trajectory))
    results[n]["unfold_and_convert"] = process_times(
        time_unfolder_and_converter(trajectory)
    )

    print("... warming up calculators")
    warmup_calculators(calculators, trajectory)

    print("... timing calculators")
    for name, calculator in calculators.items():
        print(f"...... {name}")
        times = time_calculators(calculator, trajectory)
        results[n][name] = process_times(times)

with open("results.yaml", "w") as f:
    yaml.dump(results, f)

print("done!")
