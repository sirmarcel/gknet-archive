#!/bin/bash -l

#SBATCH -J p:pre:600.2592
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
# this is custom post-processing for cheap HFs where we computed every step

cd $2/recompute




gknet out gk --freq 1.0 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 25000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 25000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 3.0 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --maxsteps 25000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 25000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc





gknet out gk --freq 1.0 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 125000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 125000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 3.0 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --maxsteps 125000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 125000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc





gknet out gk --freq 1.0 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 250000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 250000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 3.0 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --maxsteps 250000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 250000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc





gknet out gk --freq 1.0 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 375000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 375000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 3.0 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --maxsteps 375000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 375000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc





gknet out gk --freq 1.0 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 500000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --total --maxsteps 500000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 3.0 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --maxsteps 500000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --total --maxsteps 500000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc




cd ../../