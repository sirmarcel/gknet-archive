from shared import *

names_variations = {
    "jfan_mpnn": "gk_fan_mpnn_r0.every_2.to_62500.freq_1.00.nc",
    "jfan": "gk_fan_r0.every_2.to_62500.freq_1.00.nc",
    "jhardy": "gk_hardy_r0.every_2.to_62500.freq_1.00.nc",
    "junf": "gk_unfolded_r0.to_125000.every_2.freq_1.00.nc",
    "jedges": "gk_fast_transpose_r0.to_125000.every_2.freq_1.00.nc",
}

names_variations_total = {
    "jfan_mpnn": "gk_fan_mpnn_r0.every_2.total.to_62500.freq_1.00.nc",
    "jfan": "gk_fan_r0.every_2.total.to_62500.freq_1.00.nc",
    "jhardy": "gk_hardy_r0.every_2.total.to_62500.freq_1.00.nc",
    "junf": "gk_unfolded_r0.total.to_125000.every_2.freq_1.00.nc",
    "jedges": "gk_fast_transpose_r0.total.to_125000.every_2.freq_1.00.nc",
}

js = [k for k in names_variations.keys()]

thermos = ["m_300"]


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
    outfile = Path(f"hfs_m1_{thermo}.nc")
    if outfile.is_file():
        print(f"{outfile} exists, skip")
        continue

    print(f"working on {outfile.stem}")

    phase, temp = thermo.split("_")
    temp = int(temp)

    folder = Path(
        f"/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n1_s1/variations_mex_2_re_n2/300/n_768"
    )

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

