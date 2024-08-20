from numpy.random import choice, seed
from numpy import array, copy, mean, median, exp
from pandas import DataFrame
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS
from Agent import Agent
from multiprocess import Pool, cpu_count
from os import mkdir
from datetime import datetime
from utility import gen_point_mutation_dist
import time



def init_pop(pop_size, ring_pos, target, dim=3):
    """Generate an initial population of Agents

    Args:
        pop_size (int): Population size, or number of agents to generate
        ring_pos (list<(int, str)>): Initial ring positions
        target (list<(int, str)>): Target ring positions
        dim (int, optional): Dimension of the puzzle. Defaults to 3.

    Returns:
        List<Agent>: List of agents
    """

    agents = [Agent(None, ring_pos, target, d=dim) for i in range(pop_size)]

    evaluate(agents)

    return agents

def eletebetter(pop, size):

    """Select the size-th best agents in the population pop, respect to the fitness f_a.

    Args:
        pop (List<Agent>): Population of Agents
        size (int): Number of agents with highest fitness to select.

    Returns:
        List<Agent>: List of selected agents.
    """
    pop.sort(key=lambda agent:agent.fitness, reverse=True)
    return [Agent(parent.graph, parent.ring_positions, parent.target, parent.fitness, parent.move, parent.dimension) for parent in pop[:size]]


def mutate_all(pop, rate, k, levy=False) :
    """Perform for each agent in the population a move

    Args:
        pop (list<Agent>): Population of agents
        rate (float): Mutation rate
        k (int): Dimension of the faces for k-rule
        levy (bool, optional): If yes the Levy mutation is used. Defaults to False.

    Returns:
        list<Agent>: Mutation population of agents
    """
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
    """Evaluate the population agents

    Args:
        pop (list<Agent>): Population of agents
    """
    for agent in pop :
        agent.evaluate_fitnessbetter()

def select(pop, size, alpha=0.2) :
    """Roulette selection

    Args:
        pop (list<Agent>): Population of agents
        size (int): Number of agents to be selected
        alpha (float, optional): The balance between fitness and number of moves. Defaults to 0.2.

    Returns:
        list<Agent>: Population of agents
    """
    fitnesses = array([agent.selection_force(alpha) for agent in pop])
    probs = fitnesses/sum(fitnesses)
    parents = choice(pop, size=size, p=probs)

    return parents.tolist()



def save (pop, root_folder, gen):
    """Store the population

    Args:
        pop (list<Agent>): Population of agents
        root_folder (str): Path to the folder to log the population data
        gen (int): Current population generation.
    """
    data = [[agent.uid, agent.graph, agent.fitness, agent.move, agent.ring_positions] for agent in pop]
    df = DataFrame(data, columns=["ID", "graph", "fitness", "moves", "ring_positions"])
    df.to_csv(root_folder +"/gen"+str(gen)+".csv")

def evolution(params) :
    """_summary_

    Args:
        params (_type_): _description_

    Returns:
        _type_: _description_
    """
    pop_t = copy(params["pop"]).tolist()
    pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
    best = pop_t[0]
    mean_fitness = []
    max_fitnesses = [best.fitness]
    move_data = [[len(agent.move) for agent in pop_t]]
    t = 0
    tic = time.time()
    while t < params["T"] and best.fitness !=1 :

        bests = eletebetter(pop_t, int(0.1*len(pop_t)))
        selected = select(pop_t, len(pop_t)-int(0.1*len(pop_t)), params['alpha'])
        pop_t = mutate_all(selected, params["mu"], params['k'], params['levy']) + bests
        evaluate(pop_t)

        mean_ = mean([agent.fitness for agent in pop_t])
        mean_fitness += [mean_]
        pop_t.sort(key=lambda agent: agent.fitness, reverse=True)
        best = pop_t[0]
        max_fitnesses += [best.fitness]
        if params["verbose"]:
            print("generation, ", t, " max fitness : ", best.fitness, "Min moves: ", len(best.move))

        move_data += [[len(agent.move) for agent in pop_t]]
        t = t+1
    toc = time.time()

    return {"last" : pop_t,
            "mean_fitness": mean_fitness,
            "max_fitnesses": max_fitnesses,
            "best": best,
            "move_data": move_data,
            "CPU Time": toc-tic}, t

def run_ea(params):
    tic = time.time()
    best_pop = evolution(params)
    toc = time.time()
    return best_pop, toc-tic

def main():

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, argument_default=SUPPRESS)
    parser.add_argument('-mu', type=float, default=1.8, help="Mutation rate")
    parser.add_argument('-T', type=int,default=10, help="Number of generations")
    parser.add_argument('-N', type=int,default=10, help="Initial population size")
    parser.add_argument('-k', type=int, default=None, help="Move dimension. When not given, the default value is k = dimension -1")
    parser.add_argument('--job', type=int,default=1, help="Number of jobs")
    parser.add_argument('--store', action="store_true", default=False, help="store the output data")
    parser.add_argument('--print', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--alpha', type=float, default=0.15, help="balancing parameter for the selection force fitness and number of move")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")
    parser.add_argument('--levy', action="store_true", default=False, help="Use a Levy mutation scheme")

    args = parser.parse_args()

    if args.k :
        k = args.k
    else :
        k = args.dim - 1

    levels = {
    5:{
        0 : [(30, "green"), (29, "purple"), (0, "red"), (17, "blue"), (4, "yellow"), (1, "orange")]
        },
    4:{
        0 : [(4, "green"), (1, "yellow"), (5, "blue"), (7, "purple"), (13, "red")],
        1 : [(4, "purple"), (1, "yellow"), (5, "green"), (7, "blue"), (13, "red")],
        2 : [(4, "green"), (1, "yellow"), (5, "red"), (7, "blue"), (13, "purple")],
        3 : [(4, "green"), (1, "purple"), (5, "yellow"), (7, "blue"), (13, "red")],
        4 : [(4, "green"), (1, "purple"), (5, "red"), (7, "yellow"), (13, "blue")]
        },
    3:{
        0: [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")],
        1: [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")],
        2: [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")],
        3: [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]
        },
    }

    ring_pos = levels[args.dim][args.level]
    if args.dim == 3 :
        #colors = ['white', 'purple', 'white', 'white', 'green', 'red', 'blue', 'white']
        target = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        colors = ['white']*(2**args.dim)
        for i,color in target:
            colors[i] = color
    if args.dim == 4 :
        colors = ['white']*(2**args.dim)
        target = [(4, "blue"), (13, "green"), (1, "yellow"), (5, "red"), (7,"purple")]
        for i,color in target:
            colors[i] = color

    if args.dim == 5:
        colors = ['white']*(2**args.dim)
        target = [(17, "green"),(30, "purple"),(0, "red"),(29, "blue"),(4, "yellow"),(1, "orange")]

        for i,color in target:
            colors[i] = color
    if not args.levy:
        if args.mu<0 or args.mu>1.0 :
            print("When using Binomial mutation schem the parameter mu should be between 0 and 1. \nConsider adding --levy to the program call.")
            exit(1)

    print("*"*95)
    print(" "*10, "Evolutionary algorithm for solving the sliding puzzle", " "*10)
    print("*"*95)

    print("Initial ring positions: ", ring_pos)

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
        "levy": args.levy,
        "d":args.dim,
        'l': 2**args.dim - len(target),
        'level': args.level
        }]


    print(f"Solving the sliding puzzle for d={args.dim},  k={args.k}, level={args.level}...")
    print("Please, wait for few minutes....")

    pool = Pool(cpu_count())
    result = pool.map(evolution,evo_params)
    pool.close()
    best_agents = []
    storage = []
    for j in range(args.job):
        data, t = result[j]
        successful_agents = [agent for agent in data['last'] if agent.fitness == 1]
        if len(successful_agents)>0 :
            #print(j)
            successful_agents.sort(key=lambda a : len(a.move))
            best_agents += [successful_agents[0]]
            #if data['best'].fitness == 1 :
            #best_agents += [data['best']]
            storage += [{'d': evo_params[j]['d'],
                         'k': evo_params[j]['k'],
                         'l': evo_params[j]['l'],
                         't': t,
                         'level': evo_params[j]['level'],
                         'Min': len(successful_agents[0].move),
                         'Moves': successful_agents[0].move,
                         'CPU Time': data["CPU Time"]}]
    if args.store:
        #log_folder = str(datetime.now()).replace(" ", "") + '/'
        #log_folder = "../log/dim/"+str(args.dim)+"/level"+str(args.level)+"/alpha/"+str(args.alpha)+ '/'
        log_folder = "../../data/ea/dim/"+str(args.dim)+"/k/"+str(k)+"/level"+str(args.level)+"/"
        #log_folder = "../log/dim/"+str(args.dim)+"/level"+str(args.level)+"/mulevy/"+str(args.mu)+ '/'
        try:
            mkdir(log_folder)
        except Exception as e:
            pass
        print("Numner of jobs = ", len(storage))
        DataFrame(storage).to_csv(log_folder+"data_"+str(args.dim)+'_'+str(k)+"_"+str(args.level)+".csv")

    print("done.")
    print("*"*95)
    print("\n")
    print("*"*95)
    print(f"Result for d={args.dim},  k={k}, level={args.level}...")
    print("*"*95)

    if len(best_agents) > 0 :
        best_agents.sort(key=lambda a : len(a.move))
        print(f"Success rate: {len(best_agents)/args.job}")
        print(f"Median number of moves: {median([len(agent.move) for agent in best_agents])}")
        print(f"Number of moves table: {[len(a.move) for a in best_agents]}")
        print("Best agent move set: ", array(best_agents[0].move).tolist())
        print("Best agent ring positions: ", best_agents[0].ring_positions)
        print("Min number of moves: ", len(best_agents[0].move))
    print("*"*50)
if __name__ == '__main__':
    main()
