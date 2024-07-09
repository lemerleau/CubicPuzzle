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
    startState = np.array([[0, 1, 1, 1, 1],
                         [1, 0, 1, 1, 1],
                         [0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 1],
                         [0, 0, 1, 0, 0],
                         [1, 0, 0, 0, 0]])
    targetState = np.array([[1, 0, 0, 0, 1],
                         [0, 1, 1, 1, 1],
                         [0, 0, 0, 0, 0],
                         [1, 0, 1, 1, 1],
                         [0, 0, 1, 0, 0],
                         [1, 0, 0, 0, 0]])
    actualOptimal = 0
    #actualOptimal = csp.SolveCubicalSlidingPuzzle(5, 4, 26, startNodeArray = startState,
                                                  #targetNodeArray = targetState)
    
    targetState = csp.NodeState(targetState, 4, epsilon = 1)
    startState = csp.NodeState(startState, 4, targetNodeState = targetState, epsilon = 1)
    
    optimal = np.inf
    
    def DetermineWinnerRule(state, targetState = targetState):
        #if state.stateData.fcost > state.stateSpace.optimal:
        if state.stateSpace.moves > state.stateSpace.optimal:
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
        stateSpace = gl.RunGameLearn(startState, ReturnNextCubeStates, DetermineWinnerRule, 20000, permitRepeatedStates = False, targetStateData=targetState, initializationSize=100000, learningRate = .05)
    
    shifts = stateSpace.optimalShifts
    
    print(shifts)
    
    #fig, ax = plt.subplots()
    #ax.plt(stateSpace)