from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import shutil

spacing = (40000, 50001, 1000)
starts = list(reversed(range(*spacing)))
gk_run_names = list(map(lambda x: f"{x:02d}", range(len(starts))))

temperatures = [1400]
# sizes_convergence = [96, 324, 768, 1500, 2592, 4116]
sizes_convergence = [96, 324, 768, 1500, 2592, 4116]
sizes_variations_settings = [96, 768, 1500, 2592, 4116]  # where to test variations on uf
sizes_variations_cheap = [768, 1500, 2592, 4116]  # where to compute cheap variations of hf
sizes_variations_expensive = [768]  # where to compute expensive variations of hf

size_cutoffs = {300: 4116, 600: 4116, 1400: 4116}  # where to truncate convergence

environment = Environment(loader=FileSystemLoader("templates/"))

maxstepss = range(25000, 500001, 25000)


def make_temperature(temperature):

    folder = Path(f"{temperature}")
    folder.mkdir(exist_ok=True)
    shutil.rmtree(folder)
    folder.mkdir(exist_ok=True)

    for size in sizes_convergence:
        if size <= size_cutoffs[temperature]:
            f = folder / f"n_{size}"
            f.mkdir(exist_ok=True)

            (f / "nvt").mkdir(exist_ok=True)

            write_main(f, temperature, size)

    for size in sizes_variations_settings:
        f = folder / f"n_{size}"
        write_variations_settings(f, temperature, size)

    for size in sizes_variations_cheap:
        f = folder / f"n_{size}"
        write_re("ft", f, temperature, size)
        write_variations_cheap(f, temperature, size)

    for size in sizes_variations_expensive:
        f = folder / f"n_{size}"
        write_variations_expensive(f, temperature, size)


def write_main(folder, temperature, size):
    render(
        "md_nvt.in", {"temperature": temperature, "size": size}, folder / "nvt/md.in"
    )

    shutil.copy(
        f"../tetragonal_exp_real_prod_1/cells/{temperature}_geometry.in.primitive",
        folder / "nvt/geometry.in.primitive",
    )
    shutil.copy(
        f"../tetragonal_exp_real_prod_1/cells/{temperature}_geometry.in.primitive.supercell_{size}",
        folder / "nvt/geometry.in.supercell",
    )
    shutil.copy(
        f"../tetragonal_exp_real_prod_1/cells/{temperature}_geometry.in.primitive.supercell_{size}.0010K",
        folder / "nvt/geometry.in",
    )

    render("main_prep.sh", {"hours": 1}, folder / "main_prep.sh")

    render(
        "md_main.in",
        {"temperature": temperature, "size": size},
        folder / "md_main.in",
    )
    write_re("uf", folder, temperature, size)

    if size == 1500:
        hours = 6
    elif size == 2592:
        hours = 8
    elif size == 4116:
        hours = 24
    else:
        hours = 2

    render(
        "main_post.sh",
        {"temperature": temperature, "size": size, "hours": hours},
        folder / "main_post.sh",
    )

    if size == 2592:
        mins = 120
    if size == 4116:
        mins = 240
    else:
        mins = 40

    render(
        "re_post_hf.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": mins,
            "maxstepss": maxstepss,
        },
        folder / "re_post_hf.sh",
    )

    render(
        "re_post_maxsteps.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": mins,
            "maxstepss": maxstepss,
        },
        folder / "re_post_maxsteps.sh",
    )

    name = "uf"
    skin = 1.0
    skin_unfolder = 1.5
    if size == 96:
        skin = 0.075
        skin_unfolder = 0.075

    render(
        f"re_{name}.in",
        {
            "temperature": temperature,
            "size": size,
            "skin": skin,
            "skin_unfolder": skin_unfolder,
        },
        folder / f"re_{name}.in",
    )


def write_variations_settings(folder, temperature, size):
    maxstepss = [25000, 125000, 175000, 250000, 375000, 500000]

    render(
        "re_post_vs_aux.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 60,
            "maxstepss": maxstepss,
            "freqs": [1.0],
        },
        folder / "re_post_vs_aux.sh",
    )
    freqs = [0.1, 0.3, 0.5, 1, 2, 3, 5, 30]
    render(
        "re_post_vs_freq.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 60,
            "maxstepss": maxstepss,
            "freqs": freqs,
        },
        folder / "re_post_vs_freq.sh",
    )
    spacings = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    render(
        "re_post_vs_spacing.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 60,
            "maxstepss": maxstepss,
            "spacings": spacings,
            "freqs": [1.0],
        },
        folder / "re_post_vs_spacing.sh",
    )


def write_variations_expensive(folder, temperature, size):
    write_re("h", folder, temperature, size)
    write_re("f", folder, temperature, size)
    maxstepss = [12500, 62500]
    freqs = [1.0, 3.0]
    render(
        "re_post_hf_expensive.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 60,
            "maxstepss": maxstepss,
            "freqs": freqs,
        },
        folder / "re_post_hf_expensive.sh",
    )
    render(
        "re_post_fan.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 60,
            "maxstepss": maxstepss,
            "freqs": freqs,
        },
        folder / "re_post_fan.sh",
    )


def write_variations_cheap(folder, temperature, size):
    write_re("ufrt", folder, temperature, size, skin=1.0, skin_unfolder=1.5)
    write_re("e", folder, temperature, size)
    maxstepss = [25000, 125000, 250000, 375000, 500000]
    render(
        "re_post_vs_convective.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 40,
            "maxstepss": maxstepss,
            "spacings": [1, 2],
            "freqs": [1.0, 3.0],
        },
        folder / "re_post_vs_convective.sh",
    )

    render(
        "re_post_cheap.sh",
        {
            "temperature": temperature,
            "size": size,
            "mins": 40,
            "maxstepss": maxstepss,
            "freqs": [1.0, 3.0],
        },
        folder / "re_post_cheap.sh",
    )



def write_re(name, folder, temperature, size, **kwargs):

    render(
        f"re_{name}.in",
        {"temperature": temperature, "size": size, **kwargs},
        folder / f"re_{name}.in",
    )


def render(template, arguments, outfile):
    with open(outfile, "w") as f:
        f.write(environment.get_template(template).render(arguments))


for t in temperatures:
    make_temperature(t)

with open("scripts/names.txt", "w") as f:
    for name in gk_run_names:
        f.write(name + "\n")
