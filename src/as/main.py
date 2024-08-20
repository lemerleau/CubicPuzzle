#Run the A* search on the high-dimensional puzzle
import numpy as np
import time
from utils import *
from cubicgame.common import CubicalSlidingPuzzleNew as csp
import argparse
import pandas as pd
from multiprocess import Pool, cpu_count

def as_call(params):
    d = params['d']
    l = params['l']
    k = params['k']
    tgt = params['target']
    start = params['start']
    v = params['verbose']

    tic = time.time()
    actualOptimal = csp.SolveCubicalSlidingPuzzle(d, k, l,
                    startNodeArray = start,targetNodeArray = tgt, verbose=v)
    toc = time.time()

    return actualOptimal, toc-tic



def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('-k', type=int, default=None, help="Move dimension. When not given, the default value is k = dimension -1")
    parser.add_argument('--job', type=int,default=1, help="Number of jobs")
    parser.add_argument('--verbose','-v', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--save','-s', action="store_true", default=False, help="save solution data in ../data/ folder")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()

    if args.k :
        k = args.k
    else :
        k = args.dim - 1

    levels_dim4 = {
        0 : [(4, "green"), (1, "yellow"), (5, "blue"), (7, "purple"), (13, "red")],
        1 : [(4, "purple"), (1, "yellow"), (5, "green"), (7, "blue"), (13, "red")],
        2 : [(4, "green"), (1, "yellow"), (5, "red"), (7, "blue"), (13, "purple")],
        3 : [(4, "green"), (1, "purple"), (5, "yellow"), (7, "blue"), (13, "red")],
        4 : [(4, "green"), (1, "purple"), (5, "red"), (7, "yellow"), (13, "blue")]
    }

    if args.dim == 3 :
        colors = ['white', 'purple', 'white', 'white', 'green', 'red', 'blue', 'white']
        target = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        if args.level == 0 :
            start = [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")]
        if args.level == 1 :
            start = [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")]
        if args.level == 2 :
            start = [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")]
        if args.level == 3 :
            start = [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]
        if args.level == 4 :
            start = [(5, "red"), (3, "purple"), (0, "green"), (7, "blue")]

    if args.dim == 4 :
        colors = ['white']*(2**args.dim)
        colors[1] = "yellow"
        colors[4] = "blue"
        colors[5] = "red"
        colors[7] = "purple"
        colors[13] = "green"
        start = levels_dim4[args.level]
        target = [(4, "blue"), (13, "green"), (1, "yellow"), (5, "red"), (7,"purple")]

    #startState, targetState = csp.CubicalSlidingPuzzleInitialPosition(3, 2, 4, 4)
    numDict = {}
    colorDict = {}
    for i in range(2**args.dim) :
        numDict[colors[0]]= i
        colorDict[i] = colors[0]

    new_s, new_t = from_dict_to_ndarr(start, target, args.dim)
    ns = csp.NodeState(new_t, 2, epsilon = 1, colorDict = None, numDict = None)
    print("start -> {} \ntarget -> {}".format(start, target))
    print("*"*25)
    print("Results")
    print("*"*25)
    print(f"Number of jobs: {args.job}")
    params = []
    for i in range(args.job) :
        params += [{
        "job_id": i,
        'k': k,
        "start": start,
        "target": target,
        "d": args.dim,
        'l': 2**args.dim - len(target),
        'verbose': args.verbose,
        'level': args.level
        }]
    pool = Pool(cpu_count())
    outputs = pool.map(as_call, params)
    pool.close()
    rst_data = []
    for j, out in enumerate(outputs) :
        rst, cpu_time = out
        print(f"JobID: {j}, Min move: {rst[0]} finished in {cpu_time}s.")
        if rst != 0 :
            if len(rst)>0 and rst[-1] != None:
                print("List of moves")
                print("*"*25)
                listMoves = []
                cfgs = rst[-1]
                #for cfg in cfgs :
                #    print(cfg)
                for i in range(len(cfgs)-1, 0, -1):
                    listMoves += list(set(cfgs[i-1])-set(cfgs[i]))
                print(listMoves)
                print("*"*25)
                rst_data +=[{'d': params[j]['d'],
                             'k': params[j]['k'],
                             'l': params[j]['l'],
                             'level': params[j]['level'],
                             'Min': int(rst[0]),
                             'Moves': listMoves,
                             'CPU Time': cpu_time}]
    #print(rst_data)
    df_rst = pd.DataFrame(rst_data)
    if args.save :
        log_folder = "../../data/as/dim/"+str(args.dim)+"/k/"+str(k)+"/level"+str(args.level)+"/"
        df_rst.to_csv(log_folder+"as_solutions"+str(args.job)+".csv")

if __name__ == '__main__':
    main()
