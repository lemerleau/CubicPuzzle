#!/bin/bash


step=1
	for d in `seq 3 $step 5`;
	do	
		for k in `seq 1 $step $(($d-1))` ;
			do
				`python ../src/ea/main.py  -T 1000 -mu 1.8 -N 1000 --job 150 --alpha 0.2 --dim $d -k $k --level $1 --store --levy >>log_k_EA_$k.txt`
		      	echo "solved for k=: $k";
		done; 
	done; 



