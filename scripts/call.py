import plotly.offline as py
import src.black_scholes as bs
import pandas as pd


T = 1
K = 100
R = 0


def fun_set(x, s):
    return bs.call_delta(s, K, T, R, x)


sigmas = [5, 10, 20, 40, 80]

res = []
for x in range(0, 2 * K):
    res.append([fun_set(x,s/100) for s in sigmas])


deltas = pd.DataFrame(res)
deltas.columns  = ["SPOT", *sigmas]

fun_set(100, 0.3)
bs.call_delta()
