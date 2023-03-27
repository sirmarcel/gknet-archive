#!/bin/bash -l

#SBATCH -J timing
#SBATCH -o timing.%j
#SBATCH -e timing.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 96:00:00
#SBATCH --partition=p.talos

echo "starting..."
i-pi input.xml | tee ipi.out &
echo "started i-pi"
sleep 10
echo "starting ase thing..."
python run-ase.py | tee calc.out &
echo "started everything... godspeed"
wait