#!/bin/bash


step=0.2
for mu in `seq 0.2 $step 7`;	
	do 
		`python ../src/main.py --store -T 1000 -mu $mu -N 1000 --job 150 --dim 3 -k 2 --level $1 --alpha 0.2`
	      	echo "solved for mu=: $mu"; 
	done
