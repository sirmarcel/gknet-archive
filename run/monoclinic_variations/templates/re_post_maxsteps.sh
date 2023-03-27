#!/bin/bash -l

#SBATCH -J p:pre:{{ temperature }}.{{ size }}
#SBATCH -o log/p.pre.%j
#SBATCH -e log/p.pre.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 00:{{ mins }}:00
#SBATCH --partition=p.talos
        
cd $2/recompute
mkdir maxsteps_$1
{% for maxsteps in maxstepss %}
gknet out gk --freq 3.0 --maxsteps {{maxsteps}} -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps {{maxsteps}} -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps {{maxsteps}} -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc

gknet out gk --freq 3.0 --maxsteps {{maxsteps}} --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 1.0 --maxsteps {{maxsteps}} --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
gknet out gk --freq 0.3 --maxsteps {{maxsteps}} --spacing 2 -o maxsteps_$1/gk_$1.nc heat_flux_$1.nc
{% endfor %}
cd ../../
