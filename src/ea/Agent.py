
from uuid import uuid4

from numpy import random, array, where
import random as rnd
import copy
from itertools import combinations


class Agent(object):
    """docstring for Agent."""

    def __init__(self, G, pos, target, fitness=None, move=[], d=3):
        super(Agent, self).__init__()
        self.uid = str(uuid4())
        self.move = move
        self.graph = G #  a graph with n nodes, colors
        self.ring_positions = pos # list of (node, color)
        self.fitness = fitness
        self.dimension = d
        self.target = target
        self.visited = []


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
                break

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
                        for (i, r) in enumerate(ring_pos) :
                            if r[0] == node :
                                ring_pos[i] = moves[-1]
                        break
        return Agent(self.graph, ring_pos, None, moves)


    # mutating an agent means making a move
    def mutatebetter(self, rate, k) :

        ring_pos = copy.deepcopy(self.ring_positions)
        moves = copy.deepcopy(self.move)
        ring = None
        for (i, rg) in enumerate(ring_pos)  :
            if rate > random.rand() :
                ring = rg
                mut_pos = i
                # break

                # if ring :
                format_str = '{0:0'+str(self.dimension)+'b}'
                node =  ring[0]

                node_bin = format_str.format(node)
                faces = getFaces(node_bin, k)
                freenodes = []
                for face in faces :
                    fn = getFreeNodes(face, node_bin, ring_pos, self.dimension)
                    if fn:
                        freenodes += fn

                if len(freenodes)> 0 :

                    r = random.randint(0, len(freenodes))
                    moves += [(int(freenodes[r], 2), ring[-1])]
                    ring_pos [mut_pos] = (int(freenodes[r], 2), ring[-1])

        return Agent(None, ring_pos, self.target, None, moves, self.dimension)


    # mutating an agent means making a move
    def levy_mutate(self, npoints, k) :

        ring_pos = copy.deepcopy(self.ring_positions)
        moves = copy.deepcopy(self.move)
        ring = None
        rdpos = rnd.sample(range(len(ring_pos)), npoints)

        for i in rdpos:
            ring = ring_pos[i]
            mut_pos = i

            format_str = '{0:0'+str(self.dimension)+'b}'
            node =  ring[0]

            node_bin = format_str.format(node)
            faces = getFaces(node_bin, k)
            freenodes = []
            for face in faces :
                fn = getFreeNodes(face, node_bin, ring_pos, self.dimension)
                if fn:
                    freenodes += fn

            if len(freenodes)> 0 :
                #for node in freenodes :

                r = random.randint(0, len(freenodes))
                node = freenodes[r]
                #if (int(node, 2), ring[-1]) in moves:
                #    pass
                moves += [(int(node, 2), ring[-1])]
                ring_pos [mut_pos] = (int(node, 2), ring[-1])
                #    break

        return Agent(None, ring_pos, self.target, None, moves, self.dimension)

    # def mutatebetter(self, rate, k) :
    #
    #     ring_pos = copy.deepcopy(self.ring_positions)
    #     moves = copy.deepcopy(self.move)
    #     ring = None
    #     for (i, rg) in enumerate(ring_pos)  :
    #
    #         if rate > random.rand() :
    #             ring = rg
    #             mut_pos = i
    #             # break
    #
    #             # if ring :
    #             format_str = '{0:0'+str(self.dimension)+'b}'
    #             node =  ring[0]
    #
    #             node_bin = format_str.format(node)
    #             faces = getFaces(node_bin, k)
    #             freenodes = []
    #             for face in faces :
    #                 fn = getFreeNodes(face, node_bin, ring_pos, self.dimension)
    #                 if fn:
    #                     freenodes += fn
    #
    #             if len(freenodes)> 0 :
    #                 r = random.randint(0, len(freenodes))
    #                 moves += [(int(freenodes[r], 2), ring[-1])]
    #                 ring_pos [mut_pos] = (int(freenodes[r], 2), ring[-1])
    #
    #     return Agent(None, ring_pos, self.target, None, moves, self.dimension)


    def evaluate_fitness (self):
        f = 0.
        for rp in self.ring_positions :
            if rp[-1] == self.graph.nodes[rp[0]]["color"] :
                f += 1
        self.fitness = 1./(1+(len(self.ring_positions)-f))

    def evaluate_fitnessbetter (self):
        f = 0.
        # print("Target = ",self.target)
        for rp in self.ring_positions :
            if rp in self.target :
                f += 1
        self.fitness = 1./(1+(len(self.ring_positions)-f))

    def selection_force (self, alpha=0.8):
        num_moves = 1
        if len(self.move) > 0 :
            num_moves = len(self.move)

        return self.fitness*alpha + (1-alpha)*(1/(1+num_moves))


def check_move(ring_positions, nodes) :

    for ring in ring_positions :
        for node in nodes :
            if node == ring[0] :
                return False
    return True

def getFaces(node, k) :
    faces = []

    d = len(node)
    for tpl in list(combinations(range(d), k)):
        v = list(node)
        for i in tpl :
            v [i] = '*'
        faces +=[v]

    return faces

def getFaceNodes(face, node) :

    r = face.count('*')
    format_str = '{0:0'+str(r)+'b}'
    facevertices = []
    for n in range(2**r) :
        binn = format_str.format(n)
        vertex = array(face)
        idxs = where(vertex=='*') [0]
        if len(idxs) == len(binn) :
            vertex[idxs] = list(binn)
            v = "".join(vertex.tolist())
            if v != node:
                facevertices += [v]

    return facevertices

def getFreeNodes(face, node,  labelled_nodes, d):
    faceNodes = getFaceNodes(face, node)

    format_str = '{0:0'+str(d)+'b}'

    for (nd, color) in labelled_nodes :
        if format_str.format(nd) in faceNodes:
            return None
    return faceNodes
