from pathlib import Path
import shutil

base = Path("../../../gknet/experiments/")

out = Path("../train/")

out.mkdir(exist_ok=True)

for cu in [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]:
    source = base / f"ccl_zro_t96/cu_{cu:.1f}_e_inpt_4387/"
    target = out / f"cu_{cu:.1f}/"

    target.mkdir(parents=True, exist_ok=True)

    for f in source.glob("*.py"):
        shutil.copy(f, target / f.name)

    for n in [1, 2, 3]:
        source = base / f"ccl_zro_t96/cu_{cu:.1f}_e_inpt_4387/train_n{n}_s1/"
        target = out / f"cu_{cu:.1f}/m{n}/"

        shutil.copytree(source, target)

shutil.copytree(base / "oneoff/heat_flux_timings", out / "heat_flux_timings")
for p in (out / "heat_flux_timings").glob("timing.*"):
    p.unlink()

shutil.copy("README_train.md", out / "README.md")
