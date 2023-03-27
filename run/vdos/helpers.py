from pathlib import Path
from jinja2 import Environment, FileSystemLoader

temperatures = [300, 2400]

environment = Environment(loader=FileSystemLoader("templates/"))


def make_temperature(temperature):

    folder = Path(f"{temperature}")

    for ens in [0, 1, 2]:
        f = folder / str(ens)

        write_file("md.in", f, temperature)
        write_file("recompute_fast_transpose_r0.in", f, temperature)
        write_file("recompute_fast_transpose_rt.in", f, temperature)
        write_file("recompute_hardy_r0.in", f, temperature)
        write_file("recompute_hardy_rt.in", f, temperature)

        write_file("post_re_single.sh", folder, None)
        write_file("post_re_single_gk.sh", folder, None)


def write_file(file, folder, temperature):
    render(file, {"temperature": temperature}, folder / file)


def render(template, arguments, outfile):
    with open(outfile, "w") as f:
        f.write(environment.get_template(template).render(arguments))


for t in temperatures:
    make_temperature(t)
