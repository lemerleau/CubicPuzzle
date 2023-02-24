

from uuid import uuid4

from numpy import random, array, where, copy
import itertools


class Agent(object):
    """docstring for Cell."""

    def __init__(self, G, pos, fitness=None, move=[]):
        super(Agent, self).__init__()
        self.uid = str(uuid4())
        self.move = move
        self.graph = G #  a graph with n nodes, colors
        self.ring_positions = pos # list of (node, color)
        self.fitness = fitness


    # mutating an agent means making a move
    def mutate(self, rate) :
        G = self.graph
        edges = {str(n): array(list(G.edges(n)))[:,-1].tolist() for n in G.nodes}

        ring = None
        ring_pos = [rg for rg in self.ring_positions]
        moves = [mv for mv in self.move]
        for rn in ring_pos :
            if rate > random.rand() :
                ring = rn

        if ring :

            node = (ring[0])
            neighbors = edges[str(node)]
            comb = list(itertools.combinations(*[edges[str(node)]],2))

            #print(comb)
            for pr in comb :
                set1 = set(edges[str(pr[0])])
                ed = array(list(set1.intersection(edges[str(pr[1])])))
                #print(node, ed, where(ed != node))
                nodeprime = ed[where(ed != node)[0][0]]
                pos_move = list(pr) + [nodeprime]

                if check_move(ring_pos,pos_move) :
                        r = random.randint(0, len(pos_move))
                        moves += [(int(pos_move[r]), ring[-1])]
                        for (i, r) in enumerate(ring_pos):
                            if r[0] == node :
                                ring_pos[i] = moves[-1]
                        break
        return Agent(self.graph, ring_pos, None, moves)


    def evaluate_fitness (self):
        f = 0.
        for rp in self.ring_positions :
            if rp[-1] == self.graph.nodes[rp[0]]["color"] :
                f += 1

        self.fitness = 1./(1+(len(self.ring_positions)-f))


def check_move(ring_positions, nodes) :

    for ring in ring_positions :
        for node in nodes :
            if node == ring[0] :
                return False
    return True
