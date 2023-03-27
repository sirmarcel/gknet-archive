#!/bin/bash -l

#SBATCH -J p:pre:1400.96
#SBATCH -o log/p.pre.%j
#SBATCH -e log/p.pre.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 00:60:00
#SBATCH --partition=p.talos
        
cd $2/recompute



gknet out gk --freq 1.0 --spacing 2 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 3 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 3 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 3 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 3 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 3 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 3 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 4 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 4 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 4 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 4 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 4 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 4 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 5 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 5 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 5 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 5 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 5 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 5 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 6 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 6 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 6 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 6 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 6 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 6 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 7 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 7 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 7 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 7 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 7 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 7 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 8 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 8 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 8 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 8 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 8 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 8 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 9 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 9 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 9 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 9 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 9 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 9 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 10 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 10 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 10 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 10 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 10 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 10 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



cd ../../