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
# this is custom post-processing for cheap HFs where we computed every step

cd $2/recompute

{% for maxsteps in maxstepss %}
{% for freq in freqs %}

gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq {{freq}} --total --maxsteps {{maxsteps}} -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} --spacing 2 -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq {{freq}} --total --maxsteps {{maxsteps}} --spacing 2 -o gk_$1.nc heat_flux_$1.nc

{% endfor %}
{% endfor %}

cd ../../
