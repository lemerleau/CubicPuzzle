import pandas as pd
import os
import ast
import numpy as np

import matplotlib.pyplot as plt
import json
import argparse



def main() :

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('--path', type=str, default="../log/", help="Data folder")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()


    with open("../data/dim/"+str(args.dim)+"/level"+str(args.level)+"_generation.json", "r") as jsonfile :
        generations = json.load(jsonfile)
        jsonfile.close()

    with open("../data/dim/"+str(args.dim)+"/level"+str(args.level)+"_data.json", "r")as jsonfile :
        data = json.load(jsonfile)
        jsonfile.close()

    with open("../data/dim/"+str(args.dim)+"/level"+str(args.level)+"_fitness.json", "r")as jsonfile :
        fitnesses = json.load(jsonfile)
        jsonfile.close()

    mut_params = sorted(np.array(list(data.keys()), dtype=float))
    figure = plt.figure(constrained_layout=True, figsize=(7,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.plot(mut_params, [(fitnesses[str(key)].count(1)/len(fitnesses[str(key)]))*100. for key in mut_params], "o-", color="darkorange", label="Success rate")
    plt.ylabel(r"Success rate (%)", weight="bold", fontsize=14)
    plt.xlabel(r"Mutation rate ($\mu$)", weight="bold", fontsize=14)
    plt.legend(loc='lower right',bbox_to_anchor=(1, 0.5))

    ax3 = ax.twinx()
    ax3.spines["top"].set_visible(False)
    ax3.set_ylabel(r'Median number of generations',fontsize=14,weight="bold")
    ax3.plot(mut_params,[np.median(generations[str(k)]) for k in mut_params],"o-", color='deepskyblue', label="#generations")
    plt.legend(loc='lower right',bbox_to_anchor=(1, 0.6))
    plt.title("Puzzle Level "+str(args.level), fontsize=17,weight="bold")
    plt.savefig("../images/mu_success_rate_dim"+str(args.dim)+"_level" +str(args.level)+".pdf")
    plt.show()

    figure = plt.figure(constrained_layout=True, figsize=(10,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    ax.set_yscale("log")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_ylabel(r"Distribution of number of moves",weight='bold', fontsize=13)
    ax.set_xlabel(r"Mutation rate ($\mu$)",weight='bold', fontsize=13)
    ax.boxplot([data[str(key)] for key in mut_params], labels=mut_params)
    plt.title("Puzzle Level "+str(args.level), fontsize=17,weight="bold")
    plt.savefig("../images/mu_dim"+str(args.dim)+"_level"+str(args.level)+".pdf")
    plt.show()

    histo_data = data["0.3"]
    print(histo_data, set(histo_data), len(histo_data))
    figure = plt.figure(constrained_layout=True, figsize=(10,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    #ax.set_yscale("log")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel(r"Number of moves", weight='bold', fontsize=13)
    ax.set_ylabel(r"Frequencies", weight="bold", fontsize=13)
    ax.bar(list(set(histo_data)), [histo_data.count(s) for s in list(set(histo_data))],  width=.7, align='center')
    plt.title("Puzzle Level "+str(args.level), fontsize=17,weight="bold")
    ax2 = plt.axes([0.5, 0.35, 0.45, 0.5])
    ax2.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    histo_data = np.array(histo_data)
    plot_data = histo_data[histo_data<25].tolist()
    ax2.bar(list(set(plot_data)), [plot_data.count(s) for s in sorted(set(plot_data))],  width=.7, align='center')

    plt.savefig("../images/mu_0.3prime_histo_dim_"+str(args.dim)+"_level"+str(args.level)+".pdf")
    plt.show()







if __name__ == '__main__':
    main()
