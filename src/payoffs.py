import numpy as np


def call(x, K):
    return np.maximum(0, x-K)


def put(x, K):
    return np.maximum(0, K-x)


def straddle(x, K):
    return np.abs(x-K)
