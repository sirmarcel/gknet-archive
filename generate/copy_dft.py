from pathlib import Path
import shutil

base = Path("../../../gknet-aims/")

out = Path("../dft/")

out.mkdir(exist_ok=True)

kept_files = ["trajectory.son", "md_summary.pdf", "md_summary.txt"]

for t in [
    "inpt_10_0-2750_10ps_1ps",
    "inpt_1_0-1500_5ps_0.5ps",
    "inpt_2_0-3000_5ps_0.5ps",
    "inpt_3_0-1500_10ps_1ps",
    "inpt_4_0-3000_10ps_1ps",
    "inpt_5_0-750_5ps_0.5ps",
    "inpt_6_0-2250_5ps_0.5ps",
    "inpt_7_0-750_10ps_1ps",
    "inpt_8_0-2250_10ps_1ps",
    "inpt_9_0-2500_10ps_1ps",
]:
    shutil.copytree(base / f"ccl_zro_t96/{t}", out / f"train/{t}")
    for f in (out / f"train/{t}/md/").glob("*"):
        if f.name not in kept_files:
            f.unlink()

shutil.copytree(base / "ccl_zro_t96/cc_rerun/300K", out / "rerun/300K")
shutil.copytree(base / "ccl_zro_t96/relaxation", out / "train/relaxation")
shutil.copytree(
    base / "ccl_zro_t96/relaxation_symmetric", out / "train/relaxation_symmetric"
)

phonons = out / "phonons/monoclinic"

shutil.copytree(base / "new_verdi_monoclinic/relaxation", phonons / "relaxation")

for p in [
    "s2_k6_rho1e-7_cc_light",
    "s2_k6_rho1e-7_tight",
    "s3_k4_rho1e-7_cc_light",
    "s4_k2_rho1e-7_cc_light",
]:
    shutil.copytree(
        base / f"new_verdi_monoclinic/phonons/{p}",
        phonons / f"phonons/{p.replace('_rho1e-7_', '_')}",
    )

phonons = out / "phonons/tetragonal"


shutil.copytree(base / "new_fk_tetragonal/relaxation", phonons / "relaxation")

for p in [
    "s2_k6_rho1e-7_cc_light",
    "s2_k6_rho1e-7_tight",
    "s3_k4_rho1e-7_cc_light",
    "s4_k2_rho1e-7_cc_light",
]:
    shutil.copytree(
        base / f"new_fk_tetragonal/phonons/{p}",
        phonons / f"phonons/{p.replace('_rho1e-7_', '_')}",
    )


shutil.copy("README_dft.md", out / "README.md")
