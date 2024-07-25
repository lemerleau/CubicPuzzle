#Run the A* search on the high-dimensional puzzle
import numpy as np
from utils import *
import CubicalSlidingPuzzleNew as csp
import argparse





def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
    parser.add_argument('-k', type=int, default=None, help="Move dimension. When not given, the default value is k = dimension -1")
    parser.add_argument('--job', type=int,default=1, help="Number of jobs")
    parser.add_argument('--print', action="store_true", default=False, help="run in a verbose mode")
    parser.add_argument('--alpha', type=float, default=0.8, help="balancing parameter for the selection force fitness and number of move")
    parser.add_argument('--level', type=int,default=0, help="Level of the puzzle difficulty. They are four levels: 0: easy")
    parser.add_argument('--dim', type=int,default=3, help="Dimension of the puzzle. They are only two considered 3 and 4")

    args = parser.parse_args()

    if args.k :
        k = args.k
    else :
        k = args.dim - 1

    levels_dim4 = {
        0 : [(4, "green"), (1, "yellow"), (5, "blue"), (7, "purple"), (13, "red")],
        1 : [(4, "purple"), (1, "yellow"), (5, "green"), (7, "blue"), (13, "red")],
        2 : [(4, "green"), (1, "yellow"), (5, "red"), (7, "blue"), (13, "purple")],
        3 : [(4, "green"), (1, "purple"), (5, "yellow"), (7, "blue"), (13, "red")],
        4 : [(4, "green"), (1, "purple"), (5, "red"), (7, "yellow"), (13, "blue")]
    }

    if args.dim == 3 :
        colors = ['white', 'purple', 'white', 'white', 'green', 'red', 'blue', 'white']
        target = [(4, "green"), (1, "purple"), (5, "red"), (6, "blue")]
        if args.level == 0 :
            start = [(4, "red"), (1, "purple"), (5, "blue"), (6, "green")]
        if args.level == 1 :
            start = [(4, "purple"), (1, "blue"), (5, "red"), (6, "green")]
        if args.level == 2 :
            start = [(4, "red"), (1, "blue"), (5, "green"), (6, "purple")]
        if args.level == 3 :
            start = [(4, "red"), (1, "purple"), (5, "green"), (6, "blue")]
        if args.level == 4 :
            start = [(5, "red"), (3, "purple"), (0, "green"), (7, "blue")]

    if args.dim == 4 :
        colors = ['white']*(2**args.dim)
        colors[1] = "yellow"
        colors[4] = "blue"
        colors[5] = "red"
        colors[7] = "purple"
        colors[13] = "green"
        start = levels_dim4[args.level]
        target = [(4, "blue"), (13, "green"), (1, "yellow"), (5, "red"), (7,"purple")]

    #startState, targetState = csp.CubicalSlidingPuzzleInitialPosition(3, 2, 4, 4)

    new_s, new_t = from_dict_to_ndarr(start, target, args.dim)
    targetState = csp.NodeState(new_t, 2, epsilon = 1)
    startState = csp.NodeState(new_s, 2, targetNodeState = targetState, epsilon = 1)
    print(startState.nodeArray)
    print(targetState.nodeArray)
    print("start -> {} \ntarget -> {}".format(start, target))
    print("newstart -> {} \nnewtarget -> {}".format(new_s, new_t))
    print("*"*25)
    print("Game array: ", targetState.GetGameArray())



if __name__ == '__main__':
    main()
