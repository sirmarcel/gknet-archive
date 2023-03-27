from pathlib import Path
import shutil

base = Path("../../../gknet-results/data/")

out = Path("../results/")

out.mkdir(exist_ok=True)

data = out / "results"

shutil.copytree(base / "heat_flux_timings", data / "heat_flux_timings")
shutil.copytree(base / "kappa_convergence_N_t", data / "kappa_convergence_N_t")
shutil.copytree(
    base / "kappa_convergence_settings", data / "kappa_convergence_settings"
)

shutil.copytree(
    base / "kappa_monoclinic_experiment", data / "kappa_monoclinic_experiment"
)
shutil.rmtree(data / "kappa_monoclinic_experiment/archive")

shutil.copytree(
    base / "kappa_tetragonal_experiment", data / "kappa_tetragonal_experiment"
)
shutil.copytree(base / "kappa_reference", data / "kappa_reference")
shutil.copytree(base / "test_set_errors", data / "test_set_errors")

shutil.copytree(base / "vdos", data / "vdos")
shutil.rmtree(data / "vdos/archive")

shutil.copytree(base / "volume_vs_temp", data / "volume_vs_temp")

shutil.copytree(base / "phonons", data / "phonons")


shutil.copytree(base / "../tbx", out / "tbx")

shutil.copy("README_results.md", out / "README.md")
