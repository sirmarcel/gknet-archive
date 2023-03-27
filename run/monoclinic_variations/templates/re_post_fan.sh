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
# this is custom post-processing for the "expensive variants"
# which return actual virials, and are computed with step=2

cd $1/recompute
gknet out hf -o heat_flux_fan_r0.virials.every_2.nc --other_virials fan_r0/ --other_virials_key "fan_virials" --spacing 2 --nofreq --truncate ../md/trajectory/
gknet out nvhf -o heat_flux_fan_r0.every_2.nc --virials ../../reference_virials.fan.nc --spacing 2 --truncate ../md/trajectory/ heat_flux_fan_r0.virials.every_2.nc

gknet out hf -o heat_flux_fan_mpnn_r0.virials.every_2.nc --other_virials fan_r0/ --other_virials_key "fan_virials_mpnn" --spacing 2 --nofreq --truncate ../md/trajectory/
gknet out nvhf -o heat_flux_fan_mpnn_r0.every_2.nc --virials ../../reference_virials.nc --spacing 2 --truncate ../md/trajectory/ heat_flux_fan_mpnn_r0.virials.every_2.nc

{% for maxsteps in maxstepss %}
{% for freq in freqs %}

gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} --total -o gk_fan_mpnn_r0.virials.every_2.nc heat_flux_fan_mpnn_r0.virials.every_2.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} -o gk_fan_mpnn_r0.virials.every_2.nc heat_flux_fan_mpnn_r0.virials.every_2.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} --total -o gk_fan_mpnn_r0.every_2.nc heat_flux_fan_mpnn_r0.every_2.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} -o gk_fan_mpnn_r0.every_2.nc heat_flux_fan_mpnn_r0.every_2.nc


gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} --total -o gk_fan_r0.virials.every_2.nc heat_flux_fan_r0.virials.every_2.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} -o gk_fan_r0.virials.every_2.nc heat_flux_fan_r0.virials.every_2.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} --total -o gk_fan_r0.every_2.nc heat_flux_fan_r0.every_2.nc
gknet out gk --freq {{freq}} --maxsteps {{maxsteps}} -o gk_fan_r0.every_2.nc heat_flux_fan_r0.every_2.nc


{% endfor %}
{% endfor %}

cd ../../
