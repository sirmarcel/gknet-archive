#!/bin/bash -l

#SBATCH -J p:pre:600.96
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


gknet out gk --freq 1.0 --maxsteps 25000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 25000 --spacing 2 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 25000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --maxsteps 125000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 125000 --spacing 2 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 125000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --maxsteps 175000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 175000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 175000 --spacing 2 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 175000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --maxsteps 250000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 250000 --spacing 2 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 250000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --maxsteps 375000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 375000 --spacing 2 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 375000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --maxsteps 500000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 500000 --spacing 2 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps 500000 --spacing 2 -o gk_$1.nc heat_flux_$1.nc


cd ../../