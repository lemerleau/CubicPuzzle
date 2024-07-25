# -*- coding: utf-8 -*-
"""
A* pathfinding in the puzzle graph to solve the cubical sliding puzzle problem.

"""

import numpy as np
import itertools as it
import copy as c
import random

class Move:
    def __init__(self, row, flipIndices):
        """

        Parameters
        ----------
        row : int
            The row indicating the vertex to move.
        flipIndices : List<int>
            The indiced to flip.

        Returns
        -------
        None.

        """
        self.row = row
        self.flipIndices = flipIndices

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return self.row == other.row and self.flipIndices == other.flipIndices

    def __hash__(self):
        return hash((self.row, self.flipIndices))

class NodeState:
    def __init__(self, nodeArray, k, fcost = 0, hcost = 0, targetNodeState = None, parentNodeState = None, epsilon = 1):
        """


        Parameters
        ----------
        nodeArray : ndarray(d, numColors)
            Array where each colored node is a row.
        k : TYPE
            The k-rule to obey. (i.e, vertices can move across k-faces.)
        fcost : TYPE, optional
            The number of steps to reach the current nodeState from the start state. The default is 0.
        hcost : TYPE, optional
            The hamming distance to the target state. The default is 0.
        targetNodeState : TYPE, optional
            The target state. The default is None.

        Returns
        -------
        None.

        """
        self.nodeArray = nodeArray
        self.epsilon = epsilon
        self.parentNodeState = parentNodeState
        self.hashTuple = tuple(self.nodeArray.flatten())
        self.d = len(nodeArray[0])
        self.k = k
        self.fcost = fcost
        self.colorDict = {
            0 :"yellow",
            1 : "purple",
            2 : "orange",
            3 : "magenta",
            4 : "green",
            5 : "red",
            6 : "blue",
            7 : "cyan",
            8 : "brown",
            9 : "black",
            10: "white"
            }
        if targetNodeState != None:
            self.hcost = self.epsilon * np.sum(np.ceil(np.sum(np.abs(targetNodeState.nodeArray - self.nodeArray), axis = 1)/self.k))
            #self.hcost = self.epsilon * np.sum(np.ceil(np.sum(np.abs(targetNodeState.nodeArray - self.nodeArray), axis = 1)/3))
            #self.hcost = 0
            self.targetNodeState = targetNodeState
        else:
            self.targetNodeState = targetNodeState
            self.hcost = self.epsilon * hcost
        self.gcost = self.hcost + self.fcost

    def __eq__(self, other):
        if not isinstance(other, NodeState):
            return NotImplemented
        return (self.nodeArray == other.nodeArray).all()

    def __hash__(self):
        return hash(self.hashTuple)

    def UpdateHCost(self, targetNodeState):
        self.hcost = self.epsilon * np.sum(np.abs(targetNodeState.nodeArray - self.nodeArray))
        self.gcost = self.fcost + (self.hcost)

    def GetMoves(self):
        """


        Returns
        -------
        moveList : List<Move>
            Valid moves for the given nodeState. See Move class for format.

        """
        moveList = []
        faces = list(it.combinations(range(self.d), self.k))
        for i in range(len(self.nodeArray)):
            faceArray = np.delete(self.nodeArray, i, axis = 0) - self.nodeArray[i]
            for face in faces:
                rowSumFace = np.sum(np.delete(faceArray, face, axis = 1), axis = 1)
                if 0 not in rowSumFace:
                    for j in range(1,self.k+1):
                        flipIndicesList = list(it.combinations(face, j))
                        for flipIndices in flipIndicesList:
                            newMove = Move(i, flipIndices)
                            if newMove not in moveList:
                                moveList.append(newMove)
        return moveList

    def GetRandomMove(self, excludeList = []):
        #print(len(excludeList))
        rowList = list(range(len(self.nodeArray)))
        np.random.shuffle(rowList)
        attemptThese = list(it.combinations(range(self.d), self.k))
        #print(rowList)
        for row in rowList:
            np.random.shuffle(attemptThese)
            #print(attemptThese)
            faceArray = np.delete(self.nodeArray, row, axis = 0) - self.nodeArray[row]
            #print(faceArray)
            for comb in attemptThese:
                rowSumFace = np.sum(np.delete(faceArray, list(comb), axis = 1), axis = 1)
                #print(rowSumFace)
                if 0 not in rowSumFace:
                    j = np.random.randint(1, self.k+1)
                    move = tuple(random.choices(comb, k = j))
                    nextState = self.MakeMove(Move(row, move))
                    #print(nextState.nodeArray)
                    if nextState not in excludeList and nextState != self:
                        return nextState
        return None

    def MakeMove(self, move):
        """


        Parameters
        ----------
        move : Move
            The move to make.

        Returns
        -------
        newNodeState : NodeState
            The NodeState resulting from the given move.

        """
        newNodeArray = c.deepcopy(self.nodeArray)
        for i in move.flipIndices:
            newNodeArray[move.row,i] = np.mod(newNodeArray[move.row,i] + 1, 2)
        newNodeState = NodeState(newNodeArray, self.k, fcost = self.fcost + 1,
                                 targetNodeState = self.targetNodeState,
                                 parentNodeState = self, epsilon = self.epsilon)

        return newNodeState

    def GetGameArray(self):
        gameList = []
        for i in range(len(self.nodeArray)):
            out = 0
            c = 0
            for j in self.nodeArray[i]:
                out += j*(2**c)
                c += 1
            gameList.append((out, self.colorDict[out]))
        return gameList

def CubicalSlidingPuzzleInitialPosition(d, k, l, numberOfPermutations):
    numberOfColors = 2**d-l
    nodeArray = np.zeros((numberOfColors, d))
    startNodes = np.random.choice(range(2**d), numberOfColors, replace = False)
    counter = 0
    for i in startNodes:
        positionBin = list("{0:b}".format(i).zfill(d))
        nodeArray[counter] = positionBin
        counter += 1
    targetNodeArray = c.deepcopy(nodeArray)
    for i in range(numberOfPermutations):
        a, b = np.random.choice(range(len(nodeArray)), 2, replace = False)
        targetNodeArray[[a,b]] = targetNodeArray[[b,a]]
    targetNodeState = NodeState(targetNodeArray, k)
    startNodeState = NodeState(nodeArray, k, targetNodeState = targetNodeState)
    return startNodeState, targetNodeState


def SolveCubicalSlidingPuzzle(d, k, l, numberOfPermutations = 2, startNodeArray = None, targetNodeArray = None, epsilon = 1):
    """
    Parameters
    ----------
    d : Int
        The dimension of the sliding puzzle to be solved.
    k : Int
        The k-rule integer. For example, k=2 means points can only slide over free 2-faces.
    l : Int
        The number of free vertices. There will be 2^d-l colors.
    numberOfPermutations : TYPE, optional
        The number of permutations the starting position will undergo. The default is 2.
    startNodeArray : TYPE, optional
        The starting node array. Each row indicates the position of a colored vertex in the puzzle. The default is None.
    targetNodeArray : TYPE, optional
        The target node array. The default is None.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if type(startNodeArray) == np.ndarray and type(targetNodeArray) == np.ndarray: #Initializes specified nodestates
        targetNodeState = NodeState(targetNodeArray, k, epsilon = epsilon)
        startNodeState = NodeState(startNodeArray, k, targetNodeState = targetNodeState, epsilon = epsilon)
    else:
        startNodeState, targetNodeState = CubicalSlidingPuzzleInitialPosition(d, k, l, numberOfPermutations) #Runs code to get starting and target nodestates from random selection.
    print(startNodeState.nodeArray)
    print(targetNodeState.nodeArray)
    if startNodeState == targetNodeState:
        return 0
    deadList = [startNodeState] #NodeStates in the deadList cannot be branched to.
    openList = [startNodeState] #NodeStates in the openList can be branched from.
    currentNodeState = startNodeState
    while True:
        moves = currentNodeState.GetMoves()  #retrieves all valid moves from a given nodestate
        openList.remove(currentNodeState)
        deadList.append(currentNodeState)
        if currentNodeState == targetNodeState: #If the targetNodeState appears, returns the fcost to get there. This is the number of steps.
            done = currentNodeState.parentNodeState
            printNodeState = currentNodeState
            while done != None:
                print(printNodeState.GetGameArray())
                printNodeState = printNodeState.parentNodeState
                done = printNodeState
            return currentNodeState.gcost, currentNodeState
        #print(currentNodeState.nodeArray)
        for move in moves:                               #for all moves...
            #print(move.row, move.flipIndices)
            newNodeState = currentNodeState.MakeMove(move) #makes the move...
            if newNodeState not in deadList and newNodeState not in openList:
                openList.append(newNodeState)              #If the newNodeState can be branched from, adds it as a valid open point.
            elif newNodeState in openList:
                if newNodeState.fcost < openList[openList.index(newNodeState)].fcost:
                    openList.pop(openList.index(newNodeState))
                    openList.append(newNodeState)
        minScore = float('inf')
        if openList == []:
            return np.inf, None                          #If we are out of open nodes then the whole graph is dead and we cannot continue.
        for openNodeState in openList:                     #determines the next step by selecting the node with lowest combined cost.
            if openNodeState.gcost < minScore:
                minScore = openNodeState.gcost
                currentNodeState = openNodeState
