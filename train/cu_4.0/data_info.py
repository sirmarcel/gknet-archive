import numpy as np

from vibes.trajectory import reader, Trajectory

data1 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_4.son")
data2 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_3.son")
data3 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_8.son")
data4 = reader("/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_7.son")

energy = np.concatenate((data1.potential_energy, data2.potential_energy, data3.potential_energy, data4.potential_energy))
forces = np.concatenate((data1.forces, data2.forces, data3.forces, data4.forces))
stress = np.concatenate((data1.stress, data2.stress, data3.stress, data4.stress))

print(f"Energy:")
print(f"mean: {energy.mean().tolist()}")
print(f"median: {np.median(energy).tolist()}")
print(
    f"middle of range: {((energy.max() + energy.min())/2).tolist()}"
)
print(f"std: {energy.std().tolist()}")
print(
    f"range: {(energy.max() - energy.min()).tolist()}"
)

print("\n\nForces:")
print(f"mean: {forces.mean(axis=(0,1)).tolist()}")
print(f"mean (all): {forces.mean().tolist()}")
print(f"std: {forces.std(axis=(0,1)).tolist()}")
print(f"std (all): {forces.std().tolist()}")

print("\n\nStress:")
print(f"mean: {stress.mean(axis=(0)).tolist()}")
print(f"std: {stress.std(axis=(0)).tolist()}")
