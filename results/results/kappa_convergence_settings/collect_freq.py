from shared import *

freqs = [0.1, 0.3, 0.5, 1, 2, 3]
settings_to_keep = ["semi", "converged", "unconverged"]


def get_freqs(phase, temp, coords):
    n, maxsteps = coords
    return get_and_concatenate(
        lambda freq: get_mean(temp=temp, n=n, maxsteps=maxsteps, freq=freq, phase=phase),
        freqs,
        "freq",
    )


for phase, temp in [("m", 300), ("m", 600), ("m", 1400), ("t", 1400)]:
    for name, coords in convergence_coords.items():
        if name not in settings_to_keep:
            continue

        outfile = Path(f"freq_{phase}_{temp}_{name}.nc")
        if outfile.is_file():
            print(f"{outfile} exists, skip")
            continue
        
        print(f"working on {outfile.stem}")

        dataset = get_freqs(phase, temp, coords)
        dataset.to_netcdf(outfile)
