#!/bin/bash -l

#SBATCH -J p:pre:300.2592
#SBATCH -o log/p.pre.%j
#SBATCH -e log/p.pre.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 00:40:00
#SBATCH --partition=p.talos
        
cd $2/recompute
mkdir maxsteps_$1

gknet out gk --freq 3.0 --maxsteps 25000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 25000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 25000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 25000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 25000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 25000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 50000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 50000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 50000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 50000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 50000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 50000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 75000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 75000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 75000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 75000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 75000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 75000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 100000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 100000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 100000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 100000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 100000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 100000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 125000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 125000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 125000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 125000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 125000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 125000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 150000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 150000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 150000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 150000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 150000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 150000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 175000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 175000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 175000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 175000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 175000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 175000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 200000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 200000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 200000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 200000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 200000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 200000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 225000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 225000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 225000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 225000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 225000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 225000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 250000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 250000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 250000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 250000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 250000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 250000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 275000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 275000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 275000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 275000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 275000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 275000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 300000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 300000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 300000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 300000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 300000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 300000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 325000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 325000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 325000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 325000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 325000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 325000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 350000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 350000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 350000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 350000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 350000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 350000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 375000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 375000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 375000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 375000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 375000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 375000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 400000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 400000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 400000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 400000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 400000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 400000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 425000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 425000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 425000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 425000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 425000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 425000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 450000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 450000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 450000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 450000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 450000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 450000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 475000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 475000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 475000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 475000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 475000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 475000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 500000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 500000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 500000 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps 500000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 500000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps 500000 --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

cd ../../