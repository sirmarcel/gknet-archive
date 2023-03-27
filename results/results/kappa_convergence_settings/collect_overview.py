from shared import *

for phase, temp in [("m", 300), ("m", 600), ("m", 1400), ("t", 1400)]:
    for name, coords in convergence_coords.items():
        outfile = Path(f"overview_{phase}_{temp}_{name}.nc")
        if outfile.is_file():
            print(f"{outfile} exists, skip")
            continue

        n, maxsteps = coords

        if name != "converged":
            data = get_mean(
                phase=phase, temp=temp, n=n, maxsteps=maxsteps, freq=default_freq
            )
            data_total = get_mean(
                phase=phase,
                temp=temp,
                n=n,
                maxsteps=maxsteps,
                freq=default_freq,
                total=True,
            )
        else:
            data = get_ens(
                phase=phase, temp=temp, n=n, maxsteps=maxsteps, freq=default_freq
            )
            data = gk.combine(data, drop_individual=False)
            data_total = get_ens(
                phase=phase,
                temp=temp,
                n=n,
                maxsteps=maxsteps,
                freq=default_freq,
                total=True,
            )
            data_total = gk.combine(data_total, drop_individual=False)

        for key in data:
            if "heat_flux" in key:
                data[f"{key}_total"] = data_total[key]

        data.to_netcdf(outfile)

