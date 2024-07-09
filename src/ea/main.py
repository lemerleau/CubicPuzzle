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
from utility import gen_point_mutation_dist



def init_pop(pop_size, ring_pos, target, dim=3):

    """
    return an initial population of agents
    """
    agents = [Agent.Agent(None, ring_pos, target, d=dim) for i in range(pop_size)]

    evaluate(agents)

    return agents

def elete(pop, size):
    pop.sort(key=lambda agent:agent.fitness, reverse=True)
    return [Agent.Agent(parent.graph, parent.ring_positions, parent.fitness, parent.move) for parent in pop[:size]]

def eletebetter(pop, size):
    pop.sort(key=lambda agent:agent.fitness, reverse=True)
    return [Agent.Agent(parent.graph, parent.ring_positions, parent.target, parent.fitness, parent.move, parent.dimension) for parent in pop[:size]]


def mutate_all(pop, rate, k, levy=False) :
    mutated_pop = []
    if levy:
        dist = gen_point_mutation_dist(len(pop), rate,len(pop[0].ring_positions))
        for i, agent in enumerate(pop) :
            mutated_pop += [agent.levy_mutate(dist[i], k)]
    else :
        for agent in pop :
            mutated_pop += [agent.mutatebetter(rate, k)]

    return mutated_pop

def evaluate(pop) :
    for agent in pop :
        agent.evaluate_fitnessbetter()

def select(pop, size) :

    fitnesses = np.array([agent.selection_force(alpha=0.7) for agent in pop])
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
        bests = eletebetter(pop_t, int(0.1*len(pop_t)))
        selected = select(pop_t, len(pop_t)-int(0.1*len(pop_t)))
        pop_t = mutate_all(selected, params["mu"], params['k'], params['levy']) + bests
        evaluate(pop_t)

        mean_ = np.mean([agent.fitness for agent in pop_t])
        mean_fitness += [mean_]
        #print("Fitness", [agent.fitness for agent in pop_t])
        pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
        best = pop_t[0]
        max_fitnesses += [best.fitness]
        if params["verbose"]:
            print("generation, ", t, " max fitness : ", best.fitness, "Min moves: ", len(best.move))

        # for agent in pop_t :
        #     print("Moves: ",agent.move)

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
    parser.add_argument('-k', type=int, default=None, help="Move dimension. When not given, the default value is k = dimension -1")
    parser.add_argument('--job', type=int,default=1, help="Number of jobs")
    parser.add_argument('--store', action="store_true", default=False, help="store the output data")
    parser.add_argument('--print', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--alpha', type=float, default=0.8, help="balancing parameter for the selection force fitness and number of move")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()

    if args.k :
        k = args.k
    else :
        k = args.dim - 1

    #colors = ['blue', 'red', 'green', 'white', 'yellow', 'white', 'white', 'white']
    #optimal solution = [(4, "yellow"), (2, "green"), (0, "blue"), (1, "red")]

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
        target = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        if args.level == 0 :
            ring_pos = [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")]
        if args.level == 1 :
            ring_pos = [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")]
        if args.level == 2 :
            ring_pos = [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")]
        if args.level == 3 :
            ring_pos = [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]
        if args.level == 4 :
            ring_pos = [(5, "red"), (3, "purple"), (0, "green"), (7, "blue")]
            target = [(0, "green"), (4, "purple"), (2, "red"), (1, "blue")]


    if args.dim == 4 :
        colors = ['white']*(2**args.dim)
        colors[1] = "yellow"
        colors[4] = "blue"
        colors[5] = "red"
        colors[7] = "purple"
        colors[13] = "green"
        ring_pos = levels_dim4[args.level]
        target = [(4, "blue"), (13, "green"), (1, "yellow"), (5, "red"), (7,"purple")]

    print("*"*95)
    print(" "*10, "Evolutionary algorithm for solving the sliding puzzle", " "*10)
    print("*"*95)

    print("Initial ring positions: ", ring_pos)
    print("Target ring positions: ", target)
    #G = pop_0[0].graph
    #nx.draw(G,pos=nx.spring_layout(G), node_color=colors, labels={n: str(n) for n in G.nodes})
    #plt.show()

    evo_params = []
    print("Initialisation of the population of agents.....")
    pop_0 = init_pop(args.N, ring_pos, target, args.dim)

    print("Initialisation done.")
    for i in range(args.job) :
        evo_params += [{
        "pop": init_pop(args.N, ring_pos, target, args.dim),
        "mu" : args.mu,
        "T" : args.T,
        "N" : args.alpha,
        "job_id": i,
        "verbose": args.print,
        "alpha": args.alpha,
        'k': k,
        "target": target,
        "levy": True
        }]



    print("Solving the puzzle....")
    print("Please, wait for few minutes....")

    pool = Pool(cpu_count())
    result = pool.map(evolution,evo_params)
    pool.close()
    best_agents = []
    if args.store:
        #log_folder = str(datetime.now()).replace(" ", "") + '/'
        log_folder = "../log/dim/"+str(args.dim)+"/level"+str(args.level)+"/mu/"+(args.mu)+ '/'
        try:
            os.mkdir(log_folder)
        except Exception as e:
            pass

        for i in range(args.job):
            data, t = result[i]
            save(data["last"],log_folder, str(t)+"_"+str(i))


    for i in range(args.job):
        data, t = result[i]
        if data['best'].fitness == 1 :
            best_agents += [data["best"]]
    print("done.")
    print("*"*95)
    print("\n")
    print("*"*95)
    print("Results")
    print("*"*95)

    if len(best_agents) > 0 :
        best_agents.sort(key=lambda a : len(a.move))

        print("Best agent move set: ", np.array(best_agents[0].move).tolist())
        print("Best agent ring positions: ", best_agents[0].ring_positions)
        print("Min number of moves: ", len(best_agents[0].move))
    print("*"*50)
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
