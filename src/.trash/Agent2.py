from uuid import uuid4
import utility

from numpy import random, array, where, copy
import itertools


class Agent(object):
    """docstring for Cell."""

    def __init__(self, G, pos, facecollection=utility.get_facecollection(3, 2), fitness=None, move=[] ):
        super(Agent, self).__init__()
        self.uid = str(uuid4())
        self.move = move
        self.graph = G #  a graph with n nodes, colors
        self.ring_positions = pos # list of (node, color)
        self.fitness = fitness
        self.facecollection = facecollection


    # mutating an agent means making a move
    def mutate(self, rate):
        '''
        Given the current configuration, calculates all possible moves.
        If mutation happens choses one of them.
        '''
        ring_pos = copy(self.ring_positions)
        moves = [move for move in self.move]

        if random.rand() < rate:
            #calculate all possible moves
            possible_moves = []

            for ring in ring_pos:
                for face in self.facecollection[int(ring[0])]:
                    if is_empty(ring_pos, face):
                        for corner in face:
                            possible_moves += [[corner, ring[-1]]]

            #choose one of the moves at random
            r = random.randint(0, len(possible_moves))
            new_move = possible_moves[r]

            #update ring positions and move list
            moves += [new_move]
            for (i, r) in enumerate(ring_pos):
                if r[-1] == new_move[-1] :
                    ring_pos[i] = new_move
        
        return Agent(self.graph, ring_pos, self.facecollection, None, moves)


    def evaluate_fitness (self):
        f = 0.
        for rp in self.ring_positions :
            if rp[-1] == self.graph.nodes[int(rp[0])]["color"] :
                f += 1

        self.fitness = 1./(1+(len(self.ring_positions)-f))




def is_empty(ring_positions, nodes) :
    for ring in ring_positions :
        for node in nodes :
            if node == int(ring[0]) :
                return False
    return True
