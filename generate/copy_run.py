from pathlib import Path
import shutil

out = Path("../run/")

out.mkdir(exist_ok=True)

source = Path("../../../gknet-nnmd/experiments/ccl_zro_t96/skeleton/")

shutil.copytree(source / "monoclinic_exp_real_prod_1", out / "monoclinic_production")
shutil.copytree(source / "variations_mex_2", out / "monoclinic_variations")
shutil.copytree(source / "tetragonal_exp_real_prod_1", out / "tetragonal_production")
shutil.copytree(source / "variations_tex_2", out / "tetragonal_variations")

shutil.rmtree(out / "monoclinic_production/scripts")
shutil.rmtree(out / "monoclinic_variations/scripts")
shutil.rmtree(out / "tetragonal_production/scripts")
shutil.rmtree(out / "tetragonal_variations/scripts")

shutil.copytree(source / "new_phonons", out / "phonons")
shutil.copytree(source / "cc_rerun", out / "vdos")

shutil.copytree(source / "oneoff_ipi_heat_1", out / "heat")

shutil.copy("README_run.md", out / "README.md")
