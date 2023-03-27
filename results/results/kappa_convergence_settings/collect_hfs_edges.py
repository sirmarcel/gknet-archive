from shared import *

names_variations = {
    "jedges": "fast_transpose_r0",
    "junf": "unfolded_r0",
}


js = [k for k in names_variations.keys()]

thermos = ["m_300", "m_600"]
convergence_coords = {
    "converged": [1500, 250000],
    "ultra": [4116, 500000],
    "semi": [768, 125000],
}


def get_data(folder, name, convergence):
    hf_name = names_variations[name]

    if convergence == "semi":
        spacing = 2
    else:
        spacing = 1

    file_main = filename(
        hf=hf_name, total=False, spacing=spacing, freq=1.00, maxsteps=maxsteps
    )
    file_total = filename(
        hf=hf_name, total=True, spacing=spacing, freq=1.00, maxsteps=maxsteps
    )

    main = gk.combine(ensemble(folder, "recompute", file_main))

    if convergence == "semi":
        total = gk.combine(ensemble(folder, "recompute", file_total))

        for key in main:
            if "heat_flux" in key:
                main[key + "_total"] = total[key]

    return main


for thermo in thermos:
    for conv_name, settings in convergence_coords.items():
        outfile = Path(f"hfs_edges_{thermo}_{conv_name}.nc")
        if outfile.is_file():
            print(f"{outfile} exists, skip")
            continue

        print(f"working on {outfile.stem}")

        phase, temp = thermo.split("_")
        temp = int(temp)

        n, maxsteps = settings

        folder = get_folder(phase=phase, temp=temp, n=n)

        fail = False
        raw = {}
        for j in names_variations.keys():
            try:
    
                raw[j] = get_data(folder, j, conv_name)
            except FileNotFoundError as e:
                print("!!! missing file")
                print(e)
                fail = True

        if not fail:
            data = get_and_concatenate(lambda k: raw[k], js, "heat_flux")
            data.to_netcdf(outfile)
        else:
            print(f"!!! skip {outfile}, files missing")

