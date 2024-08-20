#!/bin/bash


step=1
for k in `seq 1 $step $(($1-1))`;
	do
		`python ../src/main.py  -T 1000 -mu 1.8 -N 100 --job 150 --dim $1
                                    -k $k --level $2 --alpha 0.15>>log_k_$k.txt`
	      	echo "solved for k=: $k";
	done
