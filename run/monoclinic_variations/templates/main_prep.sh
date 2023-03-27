#!/bin/bash -l

#SBATCH -J p:prep
#SBATCH -o p.prep.%j
#SBATCH -e p.prep.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t {{ hours }}:00:00
#SBATCH --partition=p.talos

gknet util virials ../../../best_model.torch nvt/geometry.in.supercell
gknet out therm -r 40000 50001 1000 nvt/md/trajectory.son
mkdir 00
cp md_main.in 00/md.in
cp nvt/geometry.in.primitive 00/
cp nvt/geometry.in.supercell 00/
mv geometry.in.50000 00/geometry.in
mkdir 01
cp md_main.in 01/md.in
cp nvt/geometry.in.primitive 01/
cp nvt/geometry.in.supercell 01/
mv geometry.in.49000 01/geometry.in
mkdir 02
cp md_main.in 02/md.in
cp nvt/geometry.in.primitive 02/
cp nvt/geometry.in.supercell 02/
mv geometry.in.48000 02/geometry.in
mkdir 03
cp md_main.in 03/md.in
cp nvt/geometry.in.primitive 03/
cp nvt/geometry.in.supercell 03/
mv geometry.in.47000 03/geometry.in
mkdir 04
cp md_main.in 04/md.in
cp nvt/geometry.in.primitive 04/
cp nvt/geometry.in.supercell 04/
mv geometry.in.46000 04/geometry.in
mkdir 05
cp md_main.in 05/md.in
cp nvt/geometry.in.primitive 05/
cp nvt/geometry.in.supercell 05/
mv geometry.in.45000 05/geometry.in
mkdir 06
cp md_main.in 06/md.in
cp nvt/geometry.in.primitive 06/
cp nvt/geometry.in.supercell 06/
mv geometry.in.44000 06/geometry.in
mkdir 07
cp md_main.in 07/md.in
cp nvt/geometry.in.primitive 07/
cp nvt/geometry.in.supercell 07/
mv geometry.in.43000 07/geometry.in
mkdir 08
cp md_main.in 08/md.in
cp nvt/geometry.in.primitive 08/
cp nvt/geometry.in.supercell 08/
mv geometry.in.42000 08/geometry.in
mkdir 09
cp md_main.in 09/md.in
cp nvt/geometry.in.primitive 09/
cp nvt/geometry.in.supercell 09/
mv geometry.in.41000 09/geometry.in
mkdir 10
cp md_main.in 10/md.in
cp nvt/geometry.in.primitive 10/
cp nvt/geometry.in.supercell 10/
mv geometry.in.40000 10/geometry.in
