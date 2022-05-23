import plotly.express as px
import numpy as np
import pandas as pd
import src.black_scholes as bs
from src.paths import geom_brownian_path
import src.option_hedger as oh
import src.colnames as n


T = 1
K = 100
R = 0
SIGMA_REAL = 0.10
SIGMA_IMPL = 0.60
S0 = 100
MU = -0.15

nOptionReal = "OptionReal"
nOptionImpl = "OptionImpl"
nOptionRealHedged = nOptionReal + "Hedged"
nOptionImplHedged = nOptionImpl + "Hedged"

rebal_tresholds = np.exp([0.025 * i for i in range(-10,10)])

res = []

for  i in range(100):
    print(i)
    # 201 / 333

    path, dt = geom_brownian_path(S0, MU, SIGMA_REAL, int(T*365), 1, 201)
    # path = [S0 for i in range(365)]
    # px.line(path).show()

    states = oh.replicate_call(SIGMA_IMPL, K, T, R, 0.5, 1*dt, path, dt, store=True)
    # states = replicate_call(SIGMA, K, T, R, list(S0 * rebal_tresholds), 100*dt, path, dt, store=True)

    sdf = pd.DataFrame(states)
    sdf[nOptionImpl] = sdf.apply(lambda x: bs.call_price(SIGMA_IMPL, K, x[nTtm], R, x[nPrice]), axis=1)
    sdf[nOptionImplHedged] = sdf[nOptionImpl] - sdf[nValo]

    if SIGMA_IMPL != SIGMA_REAL:
        sdf[nOptionReal] = sdf.apply(lambda x: bs.call_price(SIGMA_REAL, K, x[nTtm], R, x[nPrice]), axis=1)
        sdf[nOptionRealHedged] = sdf[nOptionReal] - sdf[nValo]

    px.line(sdf).show()

    res.append(sdf["OptionVsRepli"].iloc[-1])

px.histogram(res).show()

# test volatility
np.diff(np.log(path)).std()*np.sqrt(365)


# 
