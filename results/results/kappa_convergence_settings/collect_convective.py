from shared import *

# deal with different naming conventions, siiiiiigh

names_variations = {
    "j": "gk_unfolded_rt.convective_add.total.to_250000.every_2.freq_1.00.nc",
    "jconv": "gk_unfolded_rt.convective_only.to_250000.every_2.freq_1.00.nc",
    "jint": "gk_unfolded_r0.total.to_250000.every_2.freq_1.00.nc",
    "jpot": "gk_unfolded_rt.total.to_250000.every_2.freq_1.00.nc",
}

names_experiment = {
    "j": "gk_unfolded_rt.convective_add.every_2.total.to_125000.freq_1.00.nc",
    "jconv": "gk_unfolded_rt.convective_only.every_2.total.to_125000.freq_1.00.nc",
    "jint": "gk_unfolded_r0.every_2.total.to_125000.freq_1.00.nc",
    "jpot": "gk_unfolded_rt.every_2.total.to_125000.freq_1.00.nc",
}

js = [k for k in names_variations.keys()]

thermos = ["m_300", "m_600", "t_1400", "t_1500", "t_1800"]

for thermo in thermos:
    outfile = Path(f"convective_{thermo}_converged.nc")
    if outfile.is_file():
        print(f"{outfile} exists, skip")
        continue

    print(f"working on {outfile.stem}")

    phase, temp = thermo.split("_")
    temp = int(temp)

    folder = get_folder(phase=phase, temp=temp, n=1500)

    if "variations" in str(folder):
        names = names_variations
    else:
        names = names_experiment

    fail = False
    raw = {}
    for j, file in names.items():
        try:
            raw[j] = gk.combine(ensemble(folder, "recompute", file))
        except FileNotFoundError as e:
            print("!!! missing file")
            print(e)
            fail = True

    if not fail:
        data = get_and_concatenate(lambda k: raw[k], js, "heat_flux")
        data.to_netcdf(outfile)
    else:
        print(f"!!! skip {outfile}, files missing")

