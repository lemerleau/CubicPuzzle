#!/bin/bash

#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=65536
#SBATCH --partition=bdw
#SBATCH --mail-user=nonosaha@mis.mpg.de 
#SBATCH --mail-type=ALL


step=0.05
for mu in `seq 0.05 $step 1`;	
	do 

		`python ../src/cubicgame.py --store -T 1000 -mu $mu -N 1000 --job 150 --dim 4 --level $1`
	      	echo "solved for mu=: $mu", $1 ; 
	done
