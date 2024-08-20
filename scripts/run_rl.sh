#!/bin/bash


step=1
for d in `seq 3 1 5`;
do
	for k in `seq 1 $step $(($d-1))`;
		do
			`python ../src/rl/main.py  -itr 1000 -lr 0.05 -N 100 --job 150 --dim $d -k $k --level $1 --save >>log_kRL$k.txt`
		      	echo "solved for k=: $k";
		done
done
