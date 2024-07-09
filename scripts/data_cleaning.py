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

    #Log folder for experiment level 2
    root_path = args.path+"/"+str(args.dim)+"/level"+str(args.level)+"/mubetter/"
    folders = os.listdir(root_path)

    print ("Folder names : ", folders)
    data = {}
    fitnesses = {}
    generations ={}

    for f in folders :
        data[f] = []
        fitnesses[f] = []
        generations[f] = []
        files = os.listdir(root_path+f)

        for fil in files :
            df = pd.read_csv(root_path+f+"/"+fil)
            #data[f] += [max(df["fitness"].values.tolist())]
            fitnesses[f] += [max(df["fitness"].values.tolist())]
            df = df[df['fitness']==1.0]
            if len(df.values) >0 :
                data[f] += [min([len(ast.literal_eval(d)) for d in df['moves']])]

            gen = fil.split("_")[0]
            generations [f] += [int(gen[3:])]

        print("Folder, ", f, "done.")
    print(data)
    print(generations)

    with open("../data/dim/"+str(args.dim)+"/level"+str(args.level)+"_data.json", "w") as jsonfile :
        json.dump(data, jsonfile)
        jsonfile.close()

    with open("../data/dim/"+str(args.dim)+"/level"+str(args.level)+"_generation.json", "w") as jsonfile :
        json.dump(generations, jsonfile)
        jsonfile.close()

    with open("../data/dim/"+str(args.dim)+"/level"+str(args.level)+"_fitness.json", "w") as jsonfile :
        json.dump(fitnesses, jsonfile)
        jsonfile.close()




if __name__ == '__main__':
    main()
