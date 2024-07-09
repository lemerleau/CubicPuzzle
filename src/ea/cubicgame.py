import numpy as np
import pandas as pd
import argparse
import Agent
import matplotlib.pyplot as plt
import networkx as nx
from multiprocess import Pool, cpu_count
import os
from datetime import datetime
from scipy.spatial.distance import hamming




def init_pop(pop_size, ring_pos, colors, dim=3):

    """
    return an initial population of agents
    """

    G = nx.Graph()

    G.add_nodes_from(range(2**dim))
    if dim == 3 :
        edges = [(0,1), (0,3), (0,4), (1,2), (1,5), (2,3), (2,6), (3,7), (4,5), (4,7),(5,6), (6,7)]
    if dim == 4 :
        binary_vertices = ['{0:04b}'.format(u) for u in range(2**dim)]
        edges = []

        for v in binary_vertices :
            for u in binary_vertices :
                if hamming(list(v), list(u)) == 1/4. :
                    int_u = int(u, base=2)
                    int_v = int(v, base=2)
                    if (int_u, int_v) not in edges:
                        edges.append((int_v,int_u))


    G.add_edges_from(edges)

    for ed in edges :
        G.add_edge(ed[0], ed[1])

    attributes = {n: {"color": colors[n]} for n in range(2**dim)}
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
        selected = select(pop_t, len(pop_t)-int(0.1*len(pop_t)), params['alpha'])
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
    parser.add_argument('--store', action="store_true", default=False, help="store the output data")
    parser.add_argument('--print', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--alpha', type=float, default=0.8, help="balancing parameter for the selection force fitness and number of move")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()


    #colors = ['blue', 'red', 'green', 'white', 'yellow', 'white', 'white', 'white']
    # optimal solution = [(4, "blue"), (1, "yellow"), (5, "red"), (6, "purple"), (13, "green")]
    levels_dim4 = {
        0 : [(4, "green"), (1, "yellow"), (5, "blue"), (7, "purple"), (13, "red")],
        1 : [(4, "purple"), (1, "yellow"), (5, "green"), (7, "blue"), (13, "red")],
        2 : [(4, "green"), (1, "yellow"), (5, "red"), (7, "blue"), (13, "purple")],
        3 : [(4, "green"), (1, "purple"), (5, "yellow"), (7, "blue"), (13, "red")],
        4 : [(4, "green"), (1, "purple"), (5, "red"), (7, "yellow"), (13, "blue")]
    }

    if args.dim == 3 :
        colors = ['white', 'purple', 'white', 'white', 'green', 'red', 'blue', 'white']
        # optimal solution = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        if args.level == 0 :
            ring_pos = [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")]
        if args.level == 1 :
            ring_pos = [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")]
        if args.level == 2 :
            ring_pos = [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")]
        if args.level == 3 :
            ring_pos = [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]


    if args.dim == 4 :
        colors = ['white']*(2**args.dim)
        colors[1] = "yellow"
        colors[4] = "blue"
        colors[5] = "red"
        colors[7] = "purple"
        colors[13] = "green"
        ring_pos = levels_dim4[args.level]


    print("Initial ring positions: ", ring_pos)
    #G = pop_0[0].graph
    #nx.draw(G,pos=nx.spring_layout(G), node_color=colors, labels={n: str(n) for n in G.nodes})
    #plt.show()

    evo_params = []
    for i in range(args.job) :
        pop_0 = init_pop(args.N, ring_pos, colors, args.dim)
        evo_params += [{
        "pop": pop_0,
        "mu" : args.mu,
        "T" : args.T,
        "N" : args.alpha,
        "job_id": i,
        "verbose": args.print,
        "alpha": args.alpha
        }]


    print("*"*50)
    print(" "*10, "Starting the evolutionary algorithm", " "*10)

    pool = Pool(cpu_count())
    result = pool.map(evolution,evo_params)
    pool.close()
    print("*"*50)

    if args.store:
        #log_folder = str(datetime.now()).replace(" ", "") + '/'
        log_folder = "../log/dim/"+str(args.dim)+"/level"+str(args.level)+"/mu/"+str(args.mu)+ '/'
        try:
            os.mkdir(log_folder)
        except Exception as e:
            pass

        for i in range(args.job):
            data, t = result[i]
            save(data["last"],log_folder, str(t)+"_"+str(i))


    data, t = result[0]



    if data['best'].fitness == 1 :
        all_best = [agent for agent in data["last"] if agent.fitness==1]
        all_best.sort(key=lambda agent: len(agent.move))

        print("Best agent move set: ", all_best[0].move)
        print("Best agent ring positions: ", all_best[0].ring_positions)
        print("Min number of moves: ", len(all_best[0].move))

    # moves =  {}
    #
    # figure = plt.figure(constrained_layout=True, figsize=(8,4))
    # gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    # ax = figure.add_subplot(gs[0,0])
    #
    # ax.spines["right"].set_visible(False)
    # ax.spines["top"].set_visible(False)
    # ax.set_xlabel("Generation(t)", weight="bold", fontsize=13)
    # ax.set_ylabel(r"Poputation mean fitness ($f_t$)", weight="bold", fontsize=13)
    # for data, t in result :
    #     plt.plot(data["mean_fitness"], color="deepskyblue")
    # plt.plot(data["mean_fitness"], color="deepskyblue", label="Fitness")
    #
    #
    # for i in range(1, args.job) :
    #     data, t = result[i]
    #     plt.plot(data["mean_fitness"], color="deepskyblue")
    #
    # plt.legend(loc='lower right',bbox_to_anchor=(1, 0.2))
    #
    # ax2 = ax.twinx()
    # ax2.spines["top"].set_visible(False)
    # ax2.set_ylabel(r"Number of moves ", weight="bold", fontsize=13)
    # data, t = result[0]
    # plt.plot([np.mean(mvs) for mvs in data["move_data"]], label="# of moves", color="darkorange")
    # for i in range(1,args.job) :
    #     data, t = result[i]
    #     plt.plot([np.mean(mvs) for mvs in data["move_data"]], color="darkorange")
    #
    # plt.legend(loc='lower right',bbox_to_anchor=(1, 0.25))

    #ax.boxplot([moves[key] for key in moves.keys()], labels=moves.keys())

    #plt.savefig("../images/mean_fitnesses.pdf")
    # plt.show()


    # plt.plot(data["mean_fitness"], label="Mean fitness")
    # plt.plot(data["max_fitnesses"], label="Max fitness")
    # plt.legend()
    # plt.ylabel(r"Poputation mean fitness ($f_t$)")
    # plt.xlabel("Generation(t)")
    # plt.savefig("../images/mean_fitness.pdf")
    # plt.show()
if __name__ == '__main__':
    main()
