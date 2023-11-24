import pandas as pd
import os
import ast
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import json
import argparse



def main() :

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('--path', type=str, default="../log/", help="Data folder")
    parser.add_argument('-nl', type=int,default=0, help="Number of puzzle difficulties to plot. They are four possible values: 1-4")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()

    data = []
    for i in range(args.nl):
        with open("../data/dim/"+str(args.dim)+"/level"+str(i)+"_data.json", "r")as jsonfile :
            data  += [json.load(jsonfile)]
            jsonfile.close()


    figure = plt.figure(constrained_layout=True, figsize=(10,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel(r"Number of moves", weight='bold', fontsize=13)
    ax.set_ylabel(r"Frequencies", weight="bold", fontsize=13)
    plt.title("Cubic puzzle of dimension "+str(args.dim), fontsize=17,weight="bold")

    ax2 = plt.axes([0.4, 0.35, 0.45, 0.5])
    ax2.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    title_fontproperties = matplotlib.font_manager.FontProperties(weight="bold")
    for i in range(args.nl) :
        histo_data = data[i]["0.3"]
        print(histo_data, set(histo_data))
        bar = ax.bar(list(set(histo_data)), [histo_data.count(s) for s in list(set(histo_data))],  width=.7, align='center')
        bar.set_label("Level "+str(i))
        ax2.bar(sorted(set(histo_data))[:13], [histo_data.count(s) for s in sorted(set(histo_data))[:13]],  width=.7, align='center')

    ax.legend(title="Difficulty levels:", title_fontproperties=title_fontproperties)
    plt.savefig("../images/mu_0.3prime_histo_dim_"+str(args.dim)+"_alllevels.pdf")
    plt.show()







if __name__ == '__main__':
    main()
