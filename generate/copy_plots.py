from pathlib import Path
import shutil

base = Path("../../plots/")

out = Path("../plots/")

out.mkdir(exist_ok=True)


def copy_without_archive(name):
    shutil.copytree(base / f"{name}", out / f"{name}")

    if (out / f"{name}/archive").is_dir():
        shutil.rmtree(out / f"{name}/archive/")

for name in [
    "heat_flux_timings",
    "heat_flux_variants",
    "kappa_convergence_N_t",
    "kappa_convergence_settings",
    "kappa_vs_temperature",
    "phonon_band_structure",
    "test_set_errors",
    "vdos",
    "volume_vs_temperature",
]:
    copy_without_archive(name)

shutil.copytree(base / "tbx", out / "tbx")
shutil.copy(base / "gknet-paper.mlpstyle", out / "gknet-paper.mlpstyle")

shutil.copy("README_plots.md", out / "README.md")
