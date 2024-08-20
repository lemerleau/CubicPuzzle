from numpy import array as nparray, ones
from numpy.random import choice as npchoice


def nthHarmonic(N,s) :
    """Compute the nth harmonic sum

    Args:
        N (int): _description_
        s (float): Exponent 

    Returns:
        _type_: _description_
    """

    harmonic = 1.00
    for i in range(2, N + 1) :
        harmonic += 1 / i**s

    return harmonic

def zipf_rvgen(low, high, N, size, a=6.) :
    """Sample N random integers that follows a Zipf distribution with parameter a.

    Args:
        low (int): Low int range
        high (int): High int range
        N (int): Size of the sample
        size (int): _description_
        a (float, optional): Exponent. Defaults to 6..

    Returns:
        _type_: _description_
    """
    choices = nparray(range(low, high+1))
    probs = choices**(-a) / nthHarmonic(N,a)
    return npchoice(choices,p=nparray(probs)/sum(probs),size=size)

def gen_point_mutation_dist(size,c, L=4):
    """_summary_

    Args:
        size (_type_): _description_
        c (_type_): _description_
        L (int, optional): _description_. Defaults to 4.

    Returns:
        _type_: _description_
    """
    dist = []
    if c !=None :
        if 0<c<7.5:
            dist = zipf_rvgen(1,L, L, size, c)
    else :
        dist = ones(size, dtype=int)

    return dist
