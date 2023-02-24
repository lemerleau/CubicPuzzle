import numpy as np
import pandas as pd
import argparse
#import Agent
import Agent2 as Agent
import matplotlib.pyplot as plt
import networkx as nx
import utility


"""
return an initial population of Cells
"""
def init_pop(pop_size, ring_pos, colors):
    G = nx.Graph()

    for i in range(8) :
        G.add_node(i)

    edges = [(0,1), (0,2), (0,4), (1,3), (1,5), (2,3), (2,6), (3,7), (4,5), (4,6),(5,7), (6,7)]

    for ed in edges :
        G.add_edge(ed[0], ed[1])

    attributes = {n: {"color": colors[n]} for n in range(8)}
    nx.set_node_attributes(G, attributes)

    for n1,attr in G.nodes(data=True):
        print(n1,attr)

    agents = [Agent.Agent(G, ring_pos) for i in range(pop_size)]

    evaluate(agents)

    return agents

def init_pop_dim_4_3(pop_size, ring_pos, colors, facecollection):
    G = nx.Graph()

    for i in range(16) :
        G.add_node(i)

    edges = [(0,1), (0,2), (0,4), (1,3), (1,5), (2,3), (2,6), (3,7), (4,5), (4,6), (5,7), (6,7),
            (0,8), (1,9), (2,10), (3,11), (4,12), (5,13), (6,14), (7,15),
            (8,9), (8,10), (8,12), (9,11), (9,13), (10,11), (10,14), (11, 15), (12, 13), (12, 14), (13, 15), (14,15)]

    for ed in edges :
        G.add_edge(ed[0], ed[1])

    attributes = {n: {"color": colors[n]} for n in range(16)}
    nx.set_node_attributes(G, attributes)

    for n1,attr in G.nodes(data=True):
        print(n1,attr)

    agents = [Agent.Agent(G, ring_pos, facecollection= facecollection) for i in range(pop_size)]

    evaluate(agents)

    return agents

def elete(pop, size):
    pop.sort(key=lambda agent:agent.fitness, reverse=True)

    #if Using original agent, delete parent.facecollection from the arguments
    return [Agent.Agent(parent.graph, parent.ring_positions, parent.facecollection, parent.fitness, parent.move) for parent in pop[:size]]


def mutate_all(pop, rate) :
    mutated_pop = []
    for agent in pop :
        mutated_pop += [agent.mutate(rate)]

    return mutated_pop

def evaluate(pop) :
    for agent in pop :
        agent.evaluate_fitness()

def select(pop, size) :

    fitnesses = np.array([agent.fitness for agent in pop])
    probs = fitnesses/sum(fitnesses)
    parents = np.random.choice(pop, size=size, p=probs)

    return parents.tolist()


def save (pop, root_folder, gen):
    # TODO:
    return None

def evolution(pop, rate, generation, root_folder="") :

    pop_t = np.copy(pop).tolist()
    pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
    best = pop_t[0]
    mean_fitness = []
    max_fitnesses = [best.fitness]
    t = 0
    while t < generation and best.fitness !=1 :

        #print("Pop", [agent.ring_positions for agent in pop_t])
        bests = elete(pop_t, int(0.1*len(pop_t)))
        selected = select(pop_t, len(pop_t)-int(0.1*len(pop_t)))
        pop_t = mutate_all(selected, rate) + bests
        evaluate(pop_t)

        mean_ = np.mean([agent.fitness for agent in pop_t])
        mean_fitness += [mean_]
        #print("Fitness", [agent.fitness for agent in pop_t])
        pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
        best = pop_t[0]
        max_fitnesses += [best.fitness]
        print("generation, ", t, " max fitness : ", best.fitness, "Max moves: ", len(best.move))

        t = t+1


    return {"last" : pop_t,
            "mean_fitness": mean_fitness,
            "max_fitnesses": max_fitnesses,
            "best": best}


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('-mu', type=float, default=0.01, help="Mutation rate")
    parser.add_argument('-T', type=int,default=10, help="Simulation time")
    parser.add_argument('-N', type=int,default=10, help="Initial population size")
    parser.add_argument('-sd', type=float, default=0.02, help="mutation effect on the fitness")
    args = parser.parse_args()

    #initial population for dim = 3, rule = 2:
    colors = ['blue', 'red', 'green', 'white', 'yellow', 'white', 'white', 'white']

    # optimal solution = [(4, "yellow"), (2, "green"), (0, "blue"), (1, "red")]
    ring_pos = [(4, "yellow"), (1, "green"), (2, "blue"), (0, "red")]

    pop_0 = init_pop(args.N, ring_pos, colors)
    
    # #initial population for dim = 4, rule = 3:

    # colors = ['blue', 'red', 'green', 'white', 'yellow', 'white', 'white', 'white', 'purple', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    # ring_pos = [(4, "yellow"), (1, "green"), (2, "blue"), (0, "red"), (8, "purple")]
    # pop_0 = init_pop_dim_4_3(args.N, ring_pos, colors, utility.get_facecollection(4,3))

    # print("Initial ring positions: ", ring_pos)

    # G = pop_0[0].graph
    # nx.draw(G,pos=nx.spring_layout(G), node_color=colors, labels={n: str(n) for n in G.nodes})
    # plt.show()

    print("*"*50)
    print(" "*10, "Starting the evolutionary algorithm", " "*10)
    data = evolution(pop_0, args.mu, args.T)
    print("*"*50)

    print("Best agent move set: ", data["best"].move)
    print("Best agent ring positions: ", data["best"].ring_positions)

    plt.plot(data["mean_fitness"], label="Mean fitness")
    plt.plot(data["max_fitnesses"], label="Max fitness")
    plt.legend()
    plt.ylabel(r"Poputation mean fitness ($f_t$)")
    plt.xlabel("Generation(t)")
    plt.savefig("./images/mean_fitness.pdf")
    plt.show()


if __name__ == '__main__':
    main()
