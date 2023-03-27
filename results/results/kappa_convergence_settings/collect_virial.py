from shared import *


# cursed, different order of modifiers -- lmao!
def filename(hf="unfolded_r0", total=False, spacing=1, freq=1.00, maxsteps=250000):
    if not total:
        total = ""
    else:
        total = ".total"

    maxsteps = f".to_{int(maxsteps/spacing)}"

    if spacing == 1:
        spacing = ""
    else:
        spacing = f".every_{spacing}"

    freq = f".freq_{freq:.2f}"

    return f"gk_{hf}{spacing}{total}{maxsteps}{freq}.nc"


def get_ens(temp=300, n=1500, phase="m", **hfargs):
    if phase == "m":
        folder = monoclinic_folder(temp, n)
    else:
        folder = tetragonal_folder(temp, n)

    file = filename(**hfargs)

    return ensemble(folder, "recompute", file)


def get_mean(**kwargs):
    return gk.combine(get_ens(**kwargs))


for phase, temp in [("m", 300), ("m", 600), ("m", 1400), ("t", 1400)]:
    outfile = Path(f"virial_{phase}_{temp}.nc")
    if outfile.is_file():
        print(f"{outfile} exists, skip")
        continue

    print(f"working on {outfile.stem}")

    data = get_mean(
        phase=phase, temp=temp, n=768, maxsteps=125000, spacing=2, hf="hardy_r0"
    )
    data_virials = get_mean(
        phase=phase, temp=temp, n=768, maxsteps=125000, spacing=2, hf="hardy_r0.virials"
    )

    for key in data:
        if "heat_flux" in key:
            data[f"{key}_virials"] = data_virials[key]

    data.to_netcdf(outfile)

