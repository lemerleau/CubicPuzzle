import numpy as np



def from_dict_to_ndarr(init, target, d) :
    new_init = []
    new_target = []
    for i in range(len(init)) :
        new_init += [list(format(init[i][0], '0'+str(d)+'b'))]
        new_target += [list(format(target[i][0], '0'+str(d)+'b'))]

    return np.array(new_init, dtype=float), np.array(new_target, dtype=float)
