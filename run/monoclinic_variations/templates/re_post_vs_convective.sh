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
gknet out nvhf -o heat_flux_$1.nc --convective "add"  --virials ../../reference_virials.nc ../md/trajectory/ $1/
gknet out nvhf -o heat_flux_$1.nc --convective "only" --virials  ../../reference_virials.nc ../md/trajectory/ $1/
gknet out nvhf -o heat_flux_$1.nc --virials  ../../reference_virials.nc ../md/trajectory/ $1/

{% for freq in freqs %}
{% for spacing in spacings %}
{% for maxsteps in maxstepss %}
gknet out gk --freq {{freq}} --spacing {{spacing}} --maxsteps {{maxsteps}} --total -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc
gknet out gk --freq {{freq}} --spacing {{spacing}} --maxsteps {{maxsteps}} -o gk_$1.convective_add.nc heat_flux_$1.convective_add.nc

gknet out gk --freq {{freq}} --spacing {{spacing}} --maxsteps {{maxsteps}} -o gk_$1.convective_only.nc heat_flux_$1.convective_only.nc

gknet out gk --freq {{freq}} --spacing {{spacing}} --maxsteps {{maxsteps}} --total -o gk_$1.nc heat_flux_$1.nc
gknet out gk --freq {{freq}} --spacing {{spacing}} --maxsteps {{maxsteps}} -o gk_$1.nc heat_flux_$1.nc
{% endfor %}
{% endfor %}
{% endfor %}
cd ../../
