#!/bin/bash -l

#SBATCH -J relaxation|relax
#SBATCH -o log/relaxation.%j
#SBATCH -e log/relaxation.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=96
#SBATCH --ntasks-per-core=1
#SBATCH -t 0:5:00
#SBATCH --partition=exclusive

conda activate gknet_aims
vibes run relaxation relaxation.in
