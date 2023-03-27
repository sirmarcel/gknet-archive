from shared import *

names_variations = {
    "jfan_mpnn": "gk_fan_mpnn_r0.every_2.to_62500.freq_1.00.nc",
    "jfan": "gk_fan_r0.every_2.to_62500.freq_1.00.nc",
    "jhardy": "gk_hardy_r0.every_2.to_62500.freq_1.00.nc",
    "junf": "gk_unfolded_r0.to_125000.every_2.freq_1.00.nc",
}

names_variations_total = {
    "jfan_mpnn": "gk_fan_mpnn_r0.every_2.total.to_62500.freq_1.00.nc",
    "jfan": "gk_fan_r0.every_2.total.to_62500.freq_1.00.nc",
    "jhardy": "gk_hardy_r0.every_2.total.to_62500.freq_1.00.nc",
    "junf": "gk_unfolded_r0.total.to_125000.every_2.freq_1.00.nc",
}

js = [k for k in names_variations.keys()]

thermos = ["m_300", "m_600", "m_1400", "t_1400"]


def get_data(folder, name):
    file_main = names_variations[name]
    file_total = names_variations_total[name]
    main = gk.combine(ensemble(folder, "recompute", file_main))
    total = gk.combine(ensemble(folder, "recompute", file_total))

    for key in main:
        if "heat_flux" in key:
            main[key + "_total"] = total[key]

    return main


for thermo in thermos:
    outfile = Path(f"hfs_mic_{thermo}.nc")
    if outfile.is_file():
        print(f"{outfile} exists, skip")
        continue

    print(f"working on {outfile.stem}")

    phase, temp = thermo.split("_")
    temp = int(temp)

    folder = get_folder(phase=phase, temp=temp, n=768)

    fail = False
    raw = {}
    for j in names_variations.keys():
        try:
            raw[j] = get_data(folder, j)
        except FileNotFoundError as e:
            print("!!! missing file")
            print(e)
            fail = True

    if not fail:
        data = get_and_concatenate(lambda k: raw[k], js, "heat_flux")
        data.to_netcdf(outfile)
    else:
        print(f"!!! skip {outfile}, files missing")

