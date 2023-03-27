from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader

spacing = (40000, 50001, 1000)
starts = list(reversed(range(*spacing)))
gk_run_names = list(map(lambda x: f"{x:02d}", range(len(starts))))

# temperatures = [300, 450, 600, 750, 900, 1050, 1200, 1400]
temperatures = [350, 400, 1400]
sizes = [1500]


environment = Environment(loader=FileSystemLoader("templates/"))


def make_temperature(temperature):

    folder = Path(f"{temperature}")

    folder.mkdir(exist_ok=True)

    for size in sizes:
        f = folder / f"n_{size}"
        f.mkdir(exist_ok=True)

        (f / "nvt").mkdir(exist_ok=True)

        write_md_nvt(f, temperature, size)

        write_md_main(f, temperature, size)
        write_prep_main(f, size)
        write_post_main(f, temperature, size)

        write_re("uf", f, temperature, size)

        write_re_post(f, temperature, size)


def write_md_nvt(folder, temperature, size):
    render(
        "md_nvt.in", {"temperature": temperature, "size": size}, folder / "nvt/md.in"
    )

    shutil.copy("templates/geometry.in", folder / "nvt/geometry.in")
    shutil.copy(
        f"cells/{temperature}_geometry.in.primitive.supercell_{size}.0010K",
        folder / "nvt/geometry.in",
    )
    shutil.copy(
        f"cells/{temperature}_geometry.in.primitive.supercell_{size}",
        folder / "nvt/geometry.in.supercell",
    )
    shutil.copy(
        f"cells/{temperature}_geometry.in.primitive", folder / "nvt/geometry.in.primitive"
    )


def write_prep_main(folder, size):
    render("main_prep.sh", {"hours": 1}, folder / "main_prep.sh")


def write_md_main(folder, temperature, size):
    render(
        "md_main.in",
        {"temperature": temperature, "size": size},
        folder / "md_main.in",
    )


def write_post_main(folder, temperature, size):
    if size == 1500:
        hours = 3
    elif size == 2592:
        hours = 4
    else:
        hours = 1

    render(
        "main_post.sh",
        {"temperature": temperature, "size": size, "hours": hours},
        folder / "main_post.sh",
    )


def write_re(name, folder, temperature, size):

    render(
        f"re_{name}.in",
        {"temperature": temperature, "size": size},
        folder / f"re_{name}.in",
    )


def write_re_post(folder, temperature, size):
    if size == 2592:
        mins = 60
    else:
        mins = 5

    render(
        "re_post.sh",
        {"temperature": temperature, "size": size, "mins": mins},
        folder / "re_post.sh",
    )


def render(template, arguments, outfile):
    with open(outfile, "w") as f:
        f.write(environment.get_template(template).render(arguments))


for t in temperatures:
    make_temperature(t)

with open("scripts/names.txt", "w") as f:
    for name in gk_run_names:
        f.write(name + "\n")


with open("scripts/sizes.txt", "w") as f:
    for name in sizes:
        f.write(str(name) + "\n")
