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
gknet out nvhf -o heat_flux_$1.nc --convective "add"  --virials ../../reference_virials.nc ../md/trajectory/ $1/
gknet out nvhf -o heat_flux_$1.nc --convective "only" --virials  ../../reference_virials.nc ../md/trajectory/ $1/
gknet out nvhf -o heat_flux_$1.nc --virials  ../../reference_virials.nc ../md/trajectory/ $1/




gknet out gk --freq 1.0 --spacing 1 --maxsteps 25000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 25000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 25000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 25000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 125000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 125000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 125000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 125000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 250000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 250000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 250000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 250000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 375000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 375000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 375000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 375000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 500000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 500000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 500000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 1 --maxsteps 500000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 1 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 1.0 --spacing 2 --maxsteps 25000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 25000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 25000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 25000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 125000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 125000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 125000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 125000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 250000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 250000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 250000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 250000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 375000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 375000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 375000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 375000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 500000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 500000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 500000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 1.0 --spacing 2 --maxsteps 500000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --spacing 2 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc





gknet out gk --freq 3.0 --spacing 1 --maxsteps 25000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 25000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 25000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 25000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 125000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 125000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 125000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 125000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 250000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 250000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 250000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 250000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 375000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 375000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 375000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 375000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 500000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 500000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 500000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 1 --maxsteps 500000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 1 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



gknet out gk --freq 3.0 --spacing 2 --maxsteps 25000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 25000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 25000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 25000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 25000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 125000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 125000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 125000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 125000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 125000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 250000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 250000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 250000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 250000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 250000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 375000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 375000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 375000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 375000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 375000 -o gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 500000 --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 500000 -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 500000 -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq 3.0 --spacing 2 --maxsteps 500000 --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 3.0 --spacing 2 --maxsteps 500000 -o gk_$1.nc heat_flux_$1.nc



cd ../../