import numpy as np
import pandas as pd
import argparse
import Agent
import matplotlib.pyplot as plt
import networkx as nx
from multiprocess import Pool, cpu_count
import os
from datetime import datetime




"""
return an initial population of agents
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

    agents = [Agent.Agent(G, ring_pos) for i in range(pop_size)]

    evaluate(agents)

    return agents

def elete(pop, size):
    pop.sort(key=lambda agent:agent.fitness, reverse=True)
    return [Agent.Agent(parent.graph, parent.ring_positions, parent.fitness, parent.move) for parent in pop[:size]]


def mutate_all(pop, rate) :
    mutated_pop = []
    for agent in pop :
        mutated_pop += [agent.mutate(rate)]

    return mutated_pop

def evaluate(pop) :
    for agent in pop :
        agent.evaluate_fitness()

def select(pop, size, alpha=0.8) :

    fitnesses = np.array([agent.selection_force(alpha) for agent in pop])
    probs = fitnesses/sum(fitnesses)
    parents = np.random.choice(pop, size=size, p=probs)

    return parents.tolist()



def save (pop, root_folder, gen):
    data = [[agent.uid, agent.graph, agent.fitness, agent.move, agent.ring_positions] for agent in pop]
    df = pd.DataFrame(data, columns=["ID", "graph", "fitness", "moves", "ring_positions"])
    df.to_csv(root_folder +"/gen"+str(gen)+".csv")

def evolution(params) :
    np.random.seed()
    pop_t = np.copy(params["pop"]).tolist()
    pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
    best = pop_t[0]
    mean_fitness = []
    max_fitnesses = [best.fitness]
    move_data = [[len(agent.move) for agent in pop_t]]
    t = 0
    while t < params["T"] and best.fitness !=1 :

        #print("Pop", [agent.ring_positions for agent in pop_t])
        bests = elete(pop_t, int(0.1*len(pop_t)))
        selected = select(pop_t, len(pop_t)-int(0.1*len(pop_t)), params["alpha"])
        pop_t = mutate_all(selected, params["mu"]) + bests
        evaluate(pop_t)

        mean_ = np.mean([agent.fitness for agent in pop_t])
        mean_fitness += [mean_]
        #print("Fitness", [agent.fitness for agent in pop_t])
        pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
        best = pop_t[0]
        max_fitnesses += [best.fitness]
        if params["verbose"]:
            print("generation, ", t, " max fitness : ", best.fitness, "Min moves: ", len(best.move))
        move_data += [[len(agent.move) for agent in pop_t]]
        t = t+1


    return {"last" : pop_t,
            "mean_fitness": mean_fitness,
            "max_fitnesses": max_fitnesses,
            "best": best,
            "move_data": move_data}, t


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('-mu', type=float, default=0.01, help="Mutation rate")
    parser.add_argument('-T', type=int,default=10, help="Number of generations")
    parser.add_argument('-N', type=int,default=10, help="Initial population size")
    parser.add_argument('--job', type=int,default=1, help="Number of jobs")
    parser.add_argument('-s','--store', action="store_true", default=False, help="store the output data")
    parser.add_argument('-v','--pr', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--alpha', type=float, default=0.8, help="balancing parameter for the selection force fitness and number of move")
    args = parser.parse_args()


    colors = ['blue', 'red', 'green', 'white', 'yellow', 'white', 'white', 'white']

    # optimal solution = [(4, "yellow"), (2, "green"), (0, "blue"), (1, "red")]
    ring_pos = [(4, "yellow"), (1, "green"), (2, "blue"), (0, "red")]



    print("Initial ring positions: ", ring_pos)
    #G = pop_0[0].graph
    #nx.draw(G,pos=nx.spring_layout(G), node_color=colors, labels={n: str(n) for n in G.nodes})
    #plt.show()

    evo_params = []
    for i in range(args.job) :
        pop_0 = init_pop(args.N, ring_pos, colors)
        evo_params += [{
        "pop": pop_0,
        "mu" : args.mu,
        "T" : args.T,
        "N" : args.alpha,
        "job_id": i,
        "verbose": args.pr, 
        "alpha" : args.alpha
        }]


    print("*"*50)
    print(" "*10, "Starting the evolutionary algorithm", " "*10)

    pool = Pool(cpu_count())
    result = pool.map(evolution,evo_params)
    pool.close()
    print("*"*50)

    if args.store:
        #log_folder = str(datetime.now()).replace(" ", "") + '/'
        log_folder = str(args.alpha)+ '/'
        try:
            os.mkdir("../log/alpha/"+log_folder)
        except Exception as e:
            pass

        for i in range(args.job):
            data, t = result[i]
            save(data["last"],"../log/alpha/"+log_folder, str(t)+"_"+str(i))

    data, t = result[0]



    if data['best'].fitness == 1 :
        all_best = [agent for agent in data["last"] if agent.fitness==1]
        all_best.sort(key=lambda agent: len(agent.move))

        print("Best agent move set: ", all_best[0].move)
        print("Best agent ring positions: ", all_best[0].ring_positions)
        print("Min number of moves: ", len(all_best[0].move))
    #moves =  {}

    #figure = plt.figure(constrained_layout=True, figsize=(10,4))
    #gs = figure.add_gridspec(nrows=1, ncols=2, left=0.05, right=0.48, wspace=0.05)
    #ax = figure.add_subplot(gs[0,0])

    #ax.spines["right"].set_visible(False)
    #ax.spines["top"].set_visible(False)
    #ax.set_xlabel("Generation(t)")
    #ax.set_ylabel(r"Poputation mean fitness ($f_t$)")
    #for i in range(args.job) :
    #    data, t = result[i]
    #    plt.plot(data["mean_fitness"], label="Pop "+ str(i))

    #plt.legend()


    #ax = figure.add_subplot(gs[0,1])
    #ax.spines["right"].set_visible(False)
    #ax.spines["top"].set_visible(False)
    #ax.set_ylabel(r"Distribution of number of moves ($D_t$)")
    #ax.set_xlabel("Generation(t)")
    #for i in range(args.job) :
    #   data, t = result[i]
    #   moves["Job_"+str(i)] = [len(agent.move) for agent in data["last"]]

    #ax.boxplot([moves[key] for key in moves.keys()], labels=moves.keys())

    #plt.savefig("../images/mean_fitness.pdf")
    #plt.show()


    # plt.plot(data["mean_fitness"], label="Mean fitness")
    # plt.plot(data["max_fitnesses"], label="Max fitness")
    # plt.legend()
    # plt.ylabel(r"Poputation mean fitness ($f_t$)")
    # plt.xlabel("Generation(t)")
    # plt.savefig("../images/mean_fitness.pdf")
    # plt.show()
if __name__ == '__main__':
    main()
