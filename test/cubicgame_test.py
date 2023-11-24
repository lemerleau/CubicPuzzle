import numpy as np
import networkx as nx
import argparse
from scipy.spatial.distance import hamming
import itertools


def createEdges(dim):
    format_str = '{0:0'+str(dim)+'b}'
    print(format_str)
    binary_vertices = [format_str.format(u) for u in range(2**dim)]
    edges = []

    print(binary_vertices)

    for v in binary_vertices :
        for u in binary_vertices :
            if hamming(list(v), list(u)) == 1/float(dim) :
                int_u = int(u, base=2)
                int_v = int(v, base=2)
                if (int_u, int_v) not in edges:
                    edges.append((int_v,int_u))

    return edges, binary_vertices

def getFaces(cube, node, k=2) :
    faces = []
    edges = {str(n): np.array(list(cube.edges(n)))[:,-1].tolist() for n in cube.nodes}
    neighbors = edges[str(node)]

    combs = list(itertools.combinations(*[neighbors], k))

    print("List of neighbors = ", neighbors)
    for cpl in combs :
        neighs = set(edges[str(cpl[0])])
        ed = np.array(list(neighs.intersection(edges[str(cpl[1])])))

        nodeprime = ed[np.where(ed != node)[0][0]]
        face = list(cpl) + [nodeprime, node]
        faces +=[face]

    return faces

def getFaceBetter(node, k) :
    faces = []

    d = len(node)

    for tpl in list(itertools.combinations(range(d), k)):
        v = list(node)
        for i in tpl :
            v [i] = '*'
        faces +=[v]

    return faces

def getFaceNodes(face) :

    r = face.count('*')
    format_str = '{0:0'+str(r)+'b}'
    facevertices = []
    for n in range(2**r) :
        binn = format_str.format(n)
        vertex = np.array(face)
        idxs = np.where(vertex=='*') [0]
        if len(idxs) == len(binn) :
            vertex[idxs] = list(binn)
        facevertices += ["".join(vertex.tolist())]

    return facevertices

def getFreeNodes(face, labelled_nodes, d):

    faceNodes = getFaceNodes(face)

    format_str = '{0:0'+str(d)+'b}'

    for (node, color) in labelled_nodes :
        if format_str.format(node) in faceNodes:
            return None

    return faceNodes



def parse_arguments():
    """Parsing command line
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--dim', '-d', default =3, type=int, help="Dimension of the cube")

    return parser.parse_args()

def main () :
    args = parse_arguments()
    dimension = args.dim
    edges, nodes = createEdges(dimension)
    assert len(nodes) == 2** dimension, "Error when generating the nodes of the hypercube"
    assert len(edges)*2 == (2** dimension) *(dimension) , "Error when generating the nodes of the hypercube"
    print("List of edges = ", edges, len(edges), 2**dimension)

    G = nx.Graph()
    G.add_nodes_from(range(2**dimension))
    G.add_edges_from(edges)

    #faces = getFaces(G, node=1, k=2)
    node = nodes[0]
    facebetter = getFaceBetter(node, k=3)

    facenodes  = getFaceNodes(facebetter[0])



    print(f"Faces of node {node} = ", facebetter)
    print(f" Nodes of face {facebetter[0]} are:", facenodes)




if __name__ == '__main__':
    main()
