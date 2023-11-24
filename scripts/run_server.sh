#!/bin/bash

len=`expr length $1`;

step=0.05
for mu in `seq 0.05 $step 1 `;	
	do 
	`python ../src/main.py --store -T 1000 -mu $mu -N 1000 --job 150`
	      	echo "solved for mu=: $mu"; 
	done
