# -*- coding: utf-8 -*-
"""
Scalable reinforcement learning code for playing games.
"""

import random
import itertools
import numpy as np
import copy

class State:
    def __init__(self, stateData, nextStateRule, determineWinnerRule, 
                 stateSpace, lastState = None, permitRepeatedStates = True):
        """
        

        Parameters
        ----------
        stateData : Any
            Array describing the game state. Must be compatible with
            nextStateRule and determineWinnerRule.
        nextStateRule : Function(State) returns list<State>
            Function which takes State and returns valid nextStates.
        determineWinnerRule : Function(state) returns Bool
            Function determining whether a state is winning. Returns True if 
            win, False if loss, None if neither.
        stateSpace : StateSpace
            Dictionary of states and weights to be updated after outcomes.
        lastState : State, optional
            The previous state. If no state is provided, the state is assumed
            to be the first state. The default is None.

        Returns
        -------
        None.

        """
        self.stateData = stateData
        self.nextStateRule = nextStateRule
        self.determineWinnerRule = determineWinnerRule
        self.stateSpace = stateSpace
        self.lastState = lastState
        self.winState = self.determineWinnerRule(self)
        self.permitRepeatedStates = permitRepeatedStates
        self.nextStates = None
        
    def __eq__(self, other): 
        if not isinstance(other, State):
            return NotImplemented
        return self.stateData == other.stateData
    
    def __hash__(self):
        return hash(self.stateData)
    
    def GetNextState(self):
        if self.nextStates is None:
            self.nextStates = self.nextStateRule(self)
            self.nextStateWeights = [self.stateSpace.GetWeight(state) 
                                     for state in self.nextStates]
        if sum(self.nextStateWeights) == 0:
            if self.permitRepeatedStates:
                return random.choices(self.nextStates)[0]
            else:
                self.winState = False
                return self
        nextStateIndex = random.choices(range(len(self.nextStateWeights)), 
                                        self.nextStateWeights)[0]
        nextState = self.nextStates[nextStateIndex]
        if self.permitRepeatedStates == False:
            self.nextStateWeights[nextStateIndex] = 0
        return nextState
    
    def SetStateSpace(self, stateSpace):
        self.stateSpace = stateSpace
        
    def NewState(self, stateData):
        newState = State(stateData, self.nextStateRule, 
                         self.determineWinnerRule, 
                         self.stateSpace, lastState = self, 
                         permitRepeatedStates = self.permitRepeatedStates)
        return newState
    
    def ExpandTarget(self):
        stateList = []
        self.nextStates = self.nextStateRule(self)
        for state in self.nextStates:
            if state not in self.stateSpace.stateWeights:
                self.stateSpace.AdjustWeight(state, self.stateSpace.GetWeight(self)/2)
                stateList.append(state)
        return stateList
    
    def UpdateWinState(self):
        self.winState = self.determineWinnerRule(self)
                

class StateSpace:
    def __init__(self, learningRate = .05):
        self.stateWeights = dict()
        self.learningRate = learningRate
        self.optimal = np.inf
        self.optimalEndState = None
        self.optimalShifts = []
        self.runs = 0
        self.moves = 0
    
    def GetWeight(self, state):
        if state in self.stateWeights:
            return self.stateWeights[state]
        else:
            self.stateWeights[state] = .0000001
            return .0000001
    
    def AdjustWeight(self, state, newWeight):
        self.stateWeights[state] = newWeight
    
    def UpdateWeights(self, win, endState):
        self.runs += 1
        self.moves = 0
        stateList = []
        stateListPopulated = False
        currentState = endState
        while stateListPopulated == False:
            stateList.append(currentState)
            currentState = currentState.lastState
            if currentState == None:
                stateListPopulated = True
        counter = 0
        for state in stateList:
            if win == True:
                self.AdjustWeight(state, (1-self.learningRate)*self.GetWeight(state) + self.learningRate*(.95**(counter)) )
                #self.AdjustWeight(state, (1-self.learningRate)*self.GetWeight(state)+ self.learningRate*(10000000)*(.95**(counter)))
            if win == False:
                self.AdjustWeight(state, max((1-self.learningRate)*(self.GetWeight(state))*(.95**(counter)),.000000000001))
                #self.AdjustWeight(state, self.GetWeight(state)*(.95**(len(stateList)-counter)))
            counter += 1

class Player:
    def __init__(self, learningRate = 0.5):
        self.score = 0
        self.stateSpace = StateSpace(learningRate = learningRate)
        self.lastState = None
        self.wins = 0
        
    def MakeMove(self, state):
        state.stateSpace = self.stateSpace
        state.lastState = self.lastState
        self.lastState = state
        return state.GetNextState()
    
    def AdjustWeights(self, win, endState):
        self.stateSpace.UpdateWeights(win, endState)
            
def RunGameLearn(startStateData, nextStateRule, determineWinnerRule, iterations,
                 learningRate = .05, permitRepeatedStates = True, stateSpace = None, targetStateData = None, initializationSize = 0):
    
    if stateSpace == None:
        stateSpace = StateSpace(learningRate = learningRate)
    else:
        stateSpace = stateSpace
        
    if targetStateData != None:
        targetState = State(targetStateData, nextStateRule, determineWinnerRule,
                           stateSpace, permitRepeatedStates = permitRepeatedStates)
        stateSpace.AdjustWeight(targetState, 1)
        #stateSpace.AdjustWeight(targetState, 100000000)

        stateList = [targetState]
        while len(stateSpace.stateWeights.keys()) < initializationSize:
            print(len(stateSpace.stateWeights.keys()))
            newStates = []
            for state in stateList:
                newStates += state.ExpandTarget()
            stateList = newStates
                
    stateSpace.optimal = np.inf
    stateSpace.optimalShifts = []
    for i in range(iterations):
        startState = State(startStateData, nextStateRule, determineWinnerRule,
                           stateSpace, permitRepeatedStates = permitRepeatedStates)
        currentState = startState.GetNextState()
        stateSpace.moves += 1
        currentState.UpdateWinState()
        while currentState.winState == None:
            candidateState = currentState.GetNextState()
            currentState = candidateState
            stateSpace.moves += 1
            if candidateState != currentState:  
                currentState.UpdateWinState()
            print(currentState.stateData.nodeArray)
            print(currentState.winState)
        stateSpace.UpdateWeights(currentState.winState, currentState)
        currentState.winState = None
        #print(stateSpace.stateWeights.values())
        #if currentState.winState == True:
         #   break
    return stateSpace

        
def RunTournament(startStateData, nextStateRule, scoreRule, determineWinnerRule, 
                  tournaments, players, learningRate = .05, 
                  permitRepeatedStates = True, stateSpace = None):
    playerList = [Player(learningRate) for i in range(players)]
    for t in range(tournaments):
        startState = State(startStateData, nextStateRule, determineWinnerRule, StateSpace())
        for comb in itertools.combinations(playerList, 2):
            state = startState
            playerOne = playerList[comb[0]]
            playerTwo = playerList[comb[1]]
            players = (playerOne, playerTwo)
            turn = 0
            while(state.winState == None):
                lastState = copy.deepcopy(state)
                state = players[turn].MakeMove(state)
                players[turn].score = scoreRule(players[turn].score, lastState, state)
                turn = np.mod(turn + 1, 2)
            if state.winState != None:
                if players[turn].score > players[np.mod(turn + 1, 2)].score:
                    players[turn].AdjustWeights(True, state)
                    players[np.mod(turn + 1, 2)].AdjustWeights(False, 
                                                               players[np.mod(turn + 1, 2)].lastState)
                    players[turn].wins += 1
                if players[turn].score < players[np.mod(turn + 1, 2)].score:
                    players[turn].AdjustWeights(False, state)
                    players[np.mod(turn + 1, 2)].AdjustWeights(True, 
                                                               players[np.mod(turn + 1, 2)].lastState)
                    players[np.mod(turn + 1, 2)].wins += 1
    return playerList