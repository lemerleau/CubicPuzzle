import pandas as pd
import os
import ast
import numpy as np

import matplotlib.pyplot as plt


def main() :
    root_path = "../log/dim/3/level0/alpha/"
    folders = os.listdir(root_path)

    print ("Folder names : ", folders)
    data = {}
    genrations ={}
    for f in folders :
        data[f] = []
        genrations[f] = []
        files = os.listdir(root_path+f)

        for fil in files :
            df = pd.read_csv(root_path+f+"/"+fil)
            df = df[df['fitness']==1.0]
            if len(df.values) >0 :
                data[f] += [min([len(ast.literal_eval(d)) for d in df['moves']])]
                #data[f] += [max(df["fitness"].values.tolist())]
            #data[f] += [max(df["fitness"].values.tolist())]
            genrations [f] += [int(fil[3:-4])]
            #data[f] += [np.min([len(ast.literal_eval(d)) for d in df['moves']])]

        print("Folder, ", f, "done. ", len(data[f]), len(files) )


    alpha_params = sorted(np.array(list(data.keys()), dtype=float))
    # figure = plt.figure(constrained_layout=True, figsize=(7,4))
    # gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    # ax = figure.add_subplot(gs[0,0])
    # ax.spines["right"].set_visible(False)
    # ax.spines["top"].set_visible(False)
    # plt.plot(mut_params, [(data[str(key)].count(1)/len(data[str(key)]))*100. for key in mut_params], "o-", color="darkorange", label="Success rate")
    # plt.ylabel(r"Success rate (%)", weight="bold", fontsize=14)
    # plt.xlabel(r"Selection force ($\alpha$)", weight="bold", fontsize=14)
    # plt.legend(loc='lower right',bbox_to_anchor=(1, 0.5))
    #
    # ax3 = ax.twinx()
    # ax3.spines["top"].set_visible(False)
    # ax3.set_ylabel(r'Median number of generations ',fontsize=14,weight="bold")
    # ax3.plot(mut_params,[np.median(genrations[str(k)]) for k in mut_params],"o-", color='deepskyblue', label="Time")
    # plt.legend(loc='lower right',bbox_to_anchor=(1, 0.6))
    # plt.savefig("../images/alpha_success_rate.pdf")
    # plt.show()

    # figure = plt.figure(constrained_layout=True, figsize=(10,4))
    # gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    # ax = figure.add_subplot(gs[0,0])
    # ax.set_yscale("log")
    # ax.spines["right"].set_visible(False)
    # ax.spines["top"].set_visible(False)
    # ax.set_ylabel(r"Distribution of number of moves",weight='bold', fontsize=13)
    # ax.set_xlabel(r"Selection force ($\alpha$)",weight='bold', fontsize=13)
    # ax.boxplot([data[str(key)] for key in mut_params], labels=mut_params)
    #
    # plt.savefig("../images/alpha_analysis.pdf")
    # plt.show()
    figure = plt.figure(constrained_layout=True, figsize=(7,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    ax.plot(alpha_params, [data[str(alpha)].count(6) for alpha in alpha_params], "o-")
    plt.xlabel(r"Selection force ($\alpha$)", weight='bold', fontsize=13)
    plt.ylabel(r"Median number of moves", weight='bold', fontsize=13)
    ax3 = ax.twinx()
    plt.plot(alpha_params, [(len(data[str(key)])/150.)*100. for key in alpha_params], "o-", color="darkorange", label="Success rate")
    plt.ylabel(r"Success rate (%)", weight="bold", fontsize=13)
    plt.legend()
    plt.savefig("../images/success_alpha_moves.pdf")
    plt.show()
    histo_data = data["0.15"]
    print(histo_data, set(histo_data))
    figure = plt.figure(constrained_layout=True, figsize=(10,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    #ax.set_yscale("log")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel(r"Number of moves", weight='bold', fontsize=13)
    ax.set_ylabel(r"Frequencies", weight="bold", fontsize=13)
    ax.bar(list(set(histo_data)), [histo_data.count(s) for s in list(set(histo_data))],  width=.7, align='center')

    ax2 = plt.axes([0.5, 0.35, 0.45, 0.5])
    ax2.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax2.bar(list(set(histo_data))[:13], [histo_data.count(s) for s in list(set(histo_data))[:13]],  width=.7, align='center')
    #plt.savefig("../images/mu_0.85_histo.pdf")
    plt.show()







if __name__ == '__main__':
    main()
