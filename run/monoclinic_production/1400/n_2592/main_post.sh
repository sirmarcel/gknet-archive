#!/bin/bash -l

#SBATCH -J p:pmd:1400.2592
#SBATCH -o p.post.%j
#SBATCH -e p.post.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 4:00:00
#SBATCH --partition=p.talos
        
cd $1/md
gknet out md
cd ../../