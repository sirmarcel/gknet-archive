from pathlib import Path

outdir = Path("/talos/scratch/mlang/gknet/data/ccl_zro_t96/cu_5.5_e_inpt_4387/")
outdir.mkdir(parents=True, exist_ok=True)

cutoff = 5.5
offset = -3290119.2507803594  # mean
