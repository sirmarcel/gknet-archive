#!/bin/bash -l

#SBATCH -J p:pre:300.768
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
# this is custom post-processing for the "expensive variants"
# which return actual virials, and are computed with step=2

cd $2/recompute
gknet out hf -o heat_flux_$1.virials.every_2.nc --other_virials $1/ --spacing 2 --nofreq --truncate ../md/trajectory/
gknet out nvhf -o heat_flux_$1.every_2.nc --virials ../../reference_virials.nc --spacing 2 --truncate ../md/trajectory/ heat_flux_$1.virials.every_2.nc





gknet out gk --freq 1.0 --maxsteps 12500 --total -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 1.0 --maxsteps 12500 -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 1.0 --maxsteps 12500 --total -o gk_$1.every_2.nc heat_flux_$1.every_2.nc
gknet out gk --freq 1.0 --maxsteps 12500 -o gk_$1.every_2.nc heat_flux_$1.every_2.nc



gknet out gk --freq 3.0 --maxsteps 12500 --total -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 3.0 --maxsteps 12500 -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 3.0 --maxsteps 12500 --total -o gk_$1.every_2.nc heat_flux_$1.every_2.nc
gknet out gk --freq 3.0 --maxsteps 12500 -o gk_$1.every_2.nc heat_flux_$1.every_2.nc





gknet out gk --freq 1.0 --maxsteps 62500 --total -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 1.0 --maxsteps 62500 -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 1.0 --maxsteps 62500 --total -o gk_$1.every_2.nc heat_flux_$1.every_2.nc
gknet out gk --freq 1.0 --maxsteps 62500 -o gk_$1.every_2.nc heat_flux_$1.every_2.nc



gknet out gk --freq 3.0 --maxsteps 62500 --total -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 3.0 --maxsteps 62500 -o gk_$1.virials.every_2.nc heat_flux_$1.virials.every_2.nc
gknet out gk --freq 3.0 --maxsteps 62500 --total -o gk_$1.every_2.nc heat_flux_$1.every_2.nc
gknet out gk --freq 3.0 --maxsteps 62500 -o gk_$1.every_2.nc heat_flux_$1.every_2.nc




cd ../../