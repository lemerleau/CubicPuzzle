# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:45:29 2023

@author: migue
"""

import GameLearn as gl
import CubicalSlidingPuzzleNew as csp
import numpy as np
import matplotlib.pyplot as plt

def ReturnNextCubeStates(state):
    #print(vars(state))
    moves = state.stateData.GetMoves()
    nextCubeStateList = []
    for move in moves:
        nextCubeStateList.append(gl.State(state.stateData.MakeMove(move), state.nextStateRule, state.determineWinnerRule, state.stateSpace, lastState = state, permitRepeatedStates = False))
    return nextCubeStateList



if __name__=="__main__":
    #startState, targetState = csp.CubicalSlidingPuzzleInitialPosition(5, 4, 26, 4)
    
    #startState = np.array([[0., 0., 0.],[0., 0., 1.],[0., 1., 0.],[1., 0., 0.]])
    #targetState = np.array([[0., 0., 0.],[1., 1., 1.],[1., 0., 1.],[0., 1., 1.]])
    
    
    
    #startState = np.array([[0, 1, 1, 1, 1],
    #                     [1, 0, 1, 1, 1],
    #                     [0, 0, 0, 0, 0],
    #                     [1, 0, 0, 0, 1],
    #                     [0, 0, 1, 0, 0],
    #                     [1, 0, 0, 0, 0]])
    #targetState = np.array([[1, 0, 0, 0, 1],
    #                     [0, 1, 1, 1, 1],
    #                     [0, 0, 0, 0, 0],
    #                     [1, 0, 1, 1, 1],
    #                     [0, 0, 1, 0, 0],
    #                     [1, 0, 0, 0, 0]])
    actualOptimal = 0
    
    #startState = np.array([[0, 0, 1, 1, 1., 0.,],
    # [0., 0., 1., 0., 1., 1.],
    # [0., 1., 0., 0., 1., 0.],
    # [1., 0., 0., 0., 1., 0.],
    # [0., 0., 0., 0., 1., 1.],
    # [0., 1., 0., 1., 1., 1.],
    # [1., 1., 1., 1., 0., 1.]])
    #targetState = np.array([[0., 0., 0., 0., 1., 1.],
    # [0., 0., 1., 0., 1., 1.],
    # [0., 1., 0., 0., 1., 0.],
    # [1., 0., 0., 0., 1., 0.],
    # [0., 1., 0., 1., 1., 1.],
    # [0., 0., 1., 1., 1., 0.],
    # [1., 1., 1., 1., 0., 1.]])
    
    #startState = np.array([[0., 0., 0., 0., 0., 0.],
    # [1., 0., 0., 0., 0., 0.],
    # [0., 1., 0., 0., 0., 0.],
    # [0., 0., 1., 0., 0., 0.],
    # [0., 0., 0., 1., 0., 0.],
    # [0., 0., 0., 0., 1., 0.],
    # [0., 0., 0., 0., 0., 1.]])
    #targetState = np.array([[1., 0., 0., 0., 0., 0.],
    # [0., 0., 0., 0., 0., 0.],
    # [0., 0., 1., 0., 0., 0.],
    # [0., 0., 0., 0., 1., 0.],
    # [0., 0., 0., 0., 0., 1.],
    # [0., 1., 0., 0., 0., 0.],
    # [0., 0., 0., 1., 0., 0.]])
    
    ad = 3
    al = 0
    
    if ad == 3 :
        colors = ['white', 'purple', 'white', 'white', 'green', 'red', 'blue', 'white']
        # optimal solution = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        target = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        if al == 0 :
            ring_pos = [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")]
        if al == 1 :
            ring_pos = [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")]
        if al == 2 :
            ring_pos = [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")]
        if al == 3 :
            ring_pos = [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]
        if al == 4 :
            ring_pos = [(5, "red"), (3, "purple"), (0, "green"), (7, "blue")]
            target = [(0, "green"), (4, "purple"), (2, "red"), (1, "blue")]
    
    #actualOptimal = csp.SolveCubicalSlidingPuzzle(5, 4, 26, startNodeArray = startState,
                                                  #targetNodeArray = targetState)
    
    targetState = csp.NodeState(target, 2, d = ad, epsilon = 1)
    startState = csp.NodeState(ring_pos, 2, d = ad, targetNodeState = targetState, epsilon = 1)
    
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
    
    if actualOptimal != np.inf:
        stateSpace = gl.RunGameLearn(startState, ReturnNextCubeStates, DetermineWinnerRule, 1000, permitRepeatedStates = False, targetStateData=targetState, initializationSize=100, learningRate = .05)
    
    shifts = stateSpace.optimalShifts
    
    currentState = stateSpace.optimalEndState
    
    bestList = []
    
    while currentState.parentNodeState is not None:
        print(currentState.GetGameArray())
        bestList.append(currentState.GetGameArray())
        currentState = currentState.parentNodeState
        
    print(shifts)
    
    #fig, ax = plt.subplots()
    #ax.plt(stateSpace)