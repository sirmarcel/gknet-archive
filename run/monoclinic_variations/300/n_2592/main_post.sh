#!/bin/bash -l

#SBATCH -J v:pmd:300.2592
#SBATCH -o log/v.post.%j
#SBATCH -e log/v.post.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 8:00:00
#SBATCH --partition=p.talos
        
cd $1/md
gknet out md
cd ../../