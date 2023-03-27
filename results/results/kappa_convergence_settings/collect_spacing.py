from shared import *

freq = 1.00
spacings = range(1, 11)
settings_to_keep = ["semi", "converged", "unconverged"]


def get_spacings(phase, temp, coords):
    n, maxsteps = coords
    return get_and_concatenate(
        lambda spacing: get_mean(
            temp=temp,
            n=n,
            maxsteps=maxsteps,
            freq=freq,
            spacing=spacing,
            phase=phase,
        ),
        spacings,
        "spacing",
    )


for phase, temp in [("m", 300), ("m", 600), ("m", 1400), ("t", 1400)]:
    for name, coords in convergence_coords.items():
        if name not in settings_to_keep:
            continue

        outfile = Path(f"spacing_{phase}_{temp}_{name}.nc")
        if outfile.is_file():
            print(f"{outfile} exists, skip")
            continue

        print(f"working on {outfile.stem}")

        dataset = get_spacings(phase, temp, coords)
        dataset.to_netcdf(outfile)
