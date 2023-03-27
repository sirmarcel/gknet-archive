#!/bin/bash -l

#SBATCH -J p:pre:300.4116
#SBATCH -o log/p.pre.%j
#SBATCH -e log/p.pre.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 00:240:00
#SBATCH --partition=p.talos
        
cd $2/recompute
gknet out nvhf -o heat_flux_$1.nc --virials ../../reference_virials.nc ../md/trajectory/ $1/
cd ../../