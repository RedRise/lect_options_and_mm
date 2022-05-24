import numpy as np


def call(x, K):
    return np.maximum(0, x-K)


def put(x, K):
    return np.maximum(0, K-x)


def straddle(x, K):
    return np.abs(x-K)

def call_spread(x, K1, K2):
    if K1 > K2:
        return None
    return call(x,K1)-call(x,K2)

def butterfly(x, K1, K2):
    if K1 >= K2:
        return None

    mid = 0.5 * (K1+K2)
    return call(x, K1) - 2 * call(x, mid) + call(x, K2)

def digit(x, K, repli_coeff=None):
    if repli_coeff and repli_coeff > 0:
        return repli_coeff * (call(x, K) - call(x, K+1/repli_coeff))
    else:
        return 1 if x >= K else 0

def butterfly_lambda(x, K, lam):
    return lam*(call(x, K-1/lam)+call(x, K+1/lam)-2*call(x,K))