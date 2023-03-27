"""Reference data in a central location"""

import numpy as np
import io

from gknet.tbx.kurve import Kurve

cc_paper_temps = np.arange(300, 2700, 300)

cc_paper_kappas = np.array(
    [
        8.594184915645307,
        5.1027337727229565,
        4.546365921653143,
        3.169997201949584,
        3.2613788179066194,
        3.3546218708076228,
        2.826802744152861,
        2.9332686200290543,
    ]
)
cc_paper_min = np.array(
    [
        6.791576969487301,
        4.296214385381241,
        3.7251414397022184,
        2.693160335220089,
        2.925508622782415,
        3.009149122861315,
        2.445517017457439,
        2.4696113840049967,
    ]
)

cc_aims = Kurve(
    "cc_aims",
    description="Carbogno et al. (with extrapolation)",
    label="aims, 96 atoms, 3x 60ps (w/ analytic time+size extrapolation)",
)
cc_aims.add_arrays(cc_paper_temps, cc_paper_kappas, cc_paper_kappas - cc_paper_min)

cc_temps_experiment = np.array(
    [
        301.10110096960534,
        381.0188220102634,
        490.86175631863483,
        499.732825465801,
        603.9064146487262,
        693.3884552500418,
        806.3800424564536,
        900.1670123422508,
        1007.4364425399921,
        1107.4740005937315,
    ]
)
cc_kappas_experiment = np.array(
    [
        8.213971547100883,
        6.100226914860505,
        5.430484419878635,
        5.097447161845557,
        4.833020192003417,
        4.4987704647315,
        4.03895597643953,
        3.8625487238603164,
        3.727501918005585,
        3.5968142741830413,
    ]
)
cc_experiments = Kurve(
    "cc_experiments",
    description="Experimental values from CC paper",
    label="experiments (from Carbogno et al. paper)",
)
cc_experiments.add_arrays(
    cc_temps_experiment, cc_kappas_experiment, np.zeros_like(cc_kappas_experiment)
)

cc_recomputed = Kurve(
    "cc_recomputed",
    description="Raw recomputed data, 20fs timestep for hf",
    label="aims, 96 atoms, 3x 60ps (recomputed CC)",
)
cc_recomputed.add_arrays([300, 1500, 2400], [3.587, 1.865, 1.651], [0.203, 0.125, 0.048])

cc_rerun = Kurve(
    "cc_rerun",
    description="Raw rerun data, 4fs timestep for hf",
    label="aims, 96 atoms, 3x 60ps (rerun of CC, hf each step)",
)
cc_rerun.add_arrays([300, 2400], [4.132, 2.209], [0.593, 0.180])


# web plot digitiser from aps talk
data_carla = """
# temperature, kappa, std
300,7.00000,1.03175
400,5.44444,0.76190
500,4.42857,0.55556
600,3.49206,0.49206
800,2.90476,0.26984
1000,2.49206,0.19048
1200,2.14286,0.12698
1400,1.93651,0.14286
1600,1.69841,0.11111
1800,1.60317,0.09524
2000,1.58730,0.01587
"""

with io.StringIO(data_carla) as f:
    carla = np.loadtxt(f, delimiter=",")
temps_carla = carla[:, 0]
kappas_carla = carla[:, 1]
stds_carla = carla[:, 2]


verdi_mlp = Kurve(
    "verdi_mlp",
    description="Verdi et al.",
    label="vasp+ml, max. 324 atoms, max. 15x 600ps",
)
verdi_mlp.add_arrays(carla[:, 0], carla[:, 1], carla[:, 2])
