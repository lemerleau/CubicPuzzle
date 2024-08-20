#!/bin/bash


step=1
for d in `seq 3 1 5`;
do
	for k in `seq 1 $step $(($d-1))`;
		do
			`python ../src/ea/main.py  -t 1000 -lr 0.05 -N 100 --job 150 --dim $d -k $k --level $1 --store >>log_k_EA_$k.txt`
		      	echo "solved for k=: $k";
		done
done
