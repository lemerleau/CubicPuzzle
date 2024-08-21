# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:45:29 2023

@author: migue
"""

import GameLearn as gl
from cubicgame.common import CubicalSlidingPuzzleNew as csp
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
import time
import argparse
from pandas import DataFrame

def ReturnNextCubeStates(state):
    moves = state.stateData.GetMoves()
    nextCubeStateList = []
    for move in moves:
        nextCubeStateList.append(gl.State(state.stateData.MakeMove(move), state.nextStateRule, state.determineWinnerRule, state.stateSpace, lastState = state, permitRepeatedStates = False))
    return nextCubeStateList

def RunRL(param):
    ad = param['d']
    level = param['level']
    k = param['k']
    initial = param['initial']
    x = param['job_id']

    targetState = csp.NodeState(param['target'], k, d = ad, epsilon = 1)
    startState = csp.NodeState(param['start'], k, d = ad, targetNodeState = targetState, epsilon = 1)

    optimal = np.inf

    def DetermineWinnerRule(state, targetState = targetState):
        #if state.stateData.fcost > state.stateSpace.optimal:
        if state.stateSpace.moves >= state.stateSpace.optimal:
            return False
        elif state.stateData == targetState:
            """
            counter = 0
            while state.lastState != None:
                state = state.lastState
                counter += 1
            state.stateSpace.optimal = counter
            """
            state.stateSpace.optimal = state.stateSpace.moves
            state.stateSpace.optimalShifts.append([state.stateSpace.runs, state.stateSpace.optimal])
            state.stateSpace.optimalEndState = state.stateData
            return True
        else:
            return None

    #if actualOptimal != np.inf:
    tic = time.time()
    stateSpace = gl.RunGameLearn(startState, ReturnNextCubeStates, DetermineWinnerRule, param['t'], permitRepeatedStates = False, targetStateData=targetState, initializationSize= initial, learningRate = param['lr'])
    toc = time.time()

    return stateSpace.optimal + 1, toc-tic

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('-k', type=int, default=None, help="Move dimension. When not given, the default value is k = dimension -1")
    parser.add_argument('--job', type=int,default=1, help="Number of jobs")
    parser.add_argument('-itr', type=int,default=1000, help="Number of iterations")
    parser.add_argument('-N', type=int,default=100, help="Number of agents")
    parser.add_argument('-lr', type=float, default=0.05, help="RL learning rate")
    parser.add_argument('--verbose','-v', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--save','-s', action="store_true", default=False, help="save solution data in ../data/ folder")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()

    if args.k :
        k = args.k
    else :
        k = args.dim - 1

    levels = {
    5:{
        0 : [(30, "green"), (29, "purple"), (0, "red"), (17, "blue"), (4, "yellow"), (1, "orange")]
        },
    4:{
        0 : [(4, "green"), (1, "yellow"), (5, "blue"), (7, "purple"), (13, "red")],
        1 : [(4, "purple"), (1, "yellow"), (5, "green"), (7, "blue"), (13, "red")],
        2 : [(4, "green"), (1, "yellow"), (5, "red"), (7, "blue"), (13, "purple")],
        3 : [(4, "green"), (1, "purple"), (5, "yellow"), (7, "blue"), (13, "red")],
        4 : [(4, "green"), (1, "purple"), (5, "red"), (7, "yellow"), (13, "blue")]
        },
    3:{
        0: [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")],
        1: [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")],
        2: [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")],
        3: [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]
        },
    }

    try : 
        start = levels[args.dim][args.level]
    except KeyError : 
        print(f"The puzzle of dimension {args.dim} has no level {args.level}")
        exit(1)
    
    if args.dim == 3 :
        #colors = ['white', 'purple', 'white', 'white', 'green', 'red', 'blue', 'white']
        target = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        colors = ['white']*(2**args.dim)
        for i,color in target:
            colors[i] = color
    if args.dim == 4 :
        colors = ['white']*(2**args.dim)
        target = [(4, "blue"), (13, "green"), (1, "yellow"), (5, "red"), (7,"purple")]
        for i,color in target:
            colors[i] = color

    if args.dim == 5:
        colors = ['white']*(2**args.dim)
        target = [(17, "green"),(30, "purple"),(0, "red"),(29, "blue"),(4, "yellow"),(1, "orange")]

        for i,color in target:
            colors[i] = color


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
        'level': args.level,
        'initial': args.N,
        't': args.itr,
        'lr': args.lr
        }]

    with Pool(cpu_count()) as pool:
        outputs = pool.map(RunRL, params)
    pool.close()

    rst_data = []
    for j, out in enumerate(outputs) :
        rst, cpu_time = out
        print(f"JobID: {j}, Min move: {rst} finished in {cpu_time}s.")
        listMoves =[]
        if rst != np.inf :
            rst_data +=[{'d': params[j]['d'],
                         'k': params[j]['k'],
                         'l': params[j]['l'],
                         'level': params[j]['level'],
                         'Min': rst,
                         'Moves': listMoves,
                         'CPU Time': cpu_time}]
    #print(rst_data)
    df_rst = DataFrame(rst_data)
    if args.save :
        log_folder = "../data/rl/dim/"+str(args.dim)+"/k/"+str(k)+"/level"+str(args.level)+"/"
        df_rst.to_csv(log_folder+"rl_solutions"+str(args.job)+".csv")


if __name__=="__main__":
    main()
