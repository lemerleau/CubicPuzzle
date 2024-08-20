#!/bin/bash

step=0.05
for alpha in `seq 0.0 $step 1`;
	do
		`python ../src/main.py --store -T 1000 -mu 1.8 -N 1000 --job 150 --dim 3 -k 2 --level $1 --alpha $alpha`
	      	echo "solved for mu=: $alpha";
	done
