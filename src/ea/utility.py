from numpy import array as nparray
from numpy.random import choice as npchoice


def nthHarmonic(N,s) :

    harmonic = 1.00
    for i in range(2, N + 1) :
        harmonic += 1 / i**s

    return harmonic

def zipf_rvgen(low, high, N, size, a=6.) :
    choices = nparray(range(low, high+1))
    probs = choices**(-a) / nthHarmonic(N,a)
    return npchoice(choices,p=nparray(probs)/sum(probs),size=size)

def gen_point_mutation_dist(size,c, L=4):

    dist = []
    if c !=None :
        if 0<c<7.5:
            dist = zipf_rvgen(1,L, L, size, c)
    else :
        dist = ones(size, dtype=int)

    return dist
