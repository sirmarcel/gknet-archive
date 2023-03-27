#!/bin/bash -l

#SBATCH -J p:pre:2000.2592
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

gknet out nvhf -o heat_flux_$1.nc --spacing 2 --convective "only" --virials ../../reference_virials.nc ../md/trajectory/ $1/
gknet out nvhf -o heat_flux_$1.nc --spacing 2 --convective "add"  --virials ../../reference_virials.nc ../md/trajectory/ $1/
gknet out nvhf -o heat_flux_$1.nc --spacing 2 --virials  ../../reference_virials.nc ../md/trajectory/ $1/

gknet out gk --freq 1.0 --maxsteps 125000 -o gk_$1.convective_only.every_2.nc heat_flux_$1.convective_only.nc
gknet out gk --freq 1.0 --maxsteps 125000 -o gk_$1.convective_add.every_2.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --maxsteps 125000 -o gk_$1.every_2.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --maxsteps 125000 --total -o gk_$1.convective_only.every_2.nc heat_flux_$1.convective_only.nc
gknet out gk --freq 1.0 --maxsteps 125000 --total -o gk_$1.convective_add.every_2.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --maxsteps 125000 --total -o gk_$1.every_2.nc heat_flux_$1.nc

cd ../../