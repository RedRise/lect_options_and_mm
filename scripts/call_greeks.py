import plotly.offline as py
import plotly.express as px
import src.black_scholes as bs
import numpy as np
import pandas as pd
from src.paths import geom_brownian_path
from src.option_hedger import *

T = 1
K = 100
R = 0
SIGMA = 0.20
STEP = 0.05
S0 = 95
MU = 0.05

nOptionValo = "OptionValo"
nRepliVsOption = "RepliVsOption"

# 201 / 333
path, dt = geom_brownian_path(S0, MU, SIGMA, int(T*365), 1, 13)
px.line(path).show()


states = replicate_call(SIGMA, K, T, R, 0.5, 1*dt, path, dt, store=True)
# fixed_rebal = [80, 90, 95, 98, 100, 102, 105, 110, 120]
# states = call_hedger(SIGMA, K, T, R, fixed_rebal, 100*dt, path, dt, store=True)

sdf = pd.DataFrame(states)
sdf[nOptionValo + "(sigma/2)"] = sdf.apply(lambda x: bs.call_price(SIGMA/2, K, x[nTtm], R, x[nPrice]), axis=1)
sdf[nOptionValo + "(=sigma)"] = sdf.apply(lambda x: bs.call_price(SIGMA, K, x[nTtm], R, x[nPrice]), axis=1)
sdf[nOptionValo + "(sigma*2)"] = sdf.apply(lambda x: bs.call_price(SIGMA*2, K, x[nTtm], R, x[nPrice]), axis=1)

sdf[nRepliVsOption + "(sigma/2)"] = sdf[nValo] - sdf[nOptionValo + "(sigma/2)"]
sdf[nRepliVsOption + "(=sigma)"] = sdf[nValo] - sdf[nOptionValo + "(=sigma)"]
sdf[nRepliVsOption + "(sigma*2)"] = sdf[nValo] - sdf[nOptionValo + "(sigma*2)"]

px.line(sdf).show()

sdf.iloc[250:265]
sdf.iloc[180:190]

# res = []
# for i in range(200):
#     if i % 10 == 0:
#         print(i)
#     path, dt = geom_brownian_path(S0, MU, SIGMA, int(T*365), 1, 201)
#     state = call_hedger(SIGMA, K, T, R, 0.025, 5*dt, path, dt, False)
#     res.append(state[nOptionValo]-state[nValo])

# px.histogram(res).show()

# Controle de la volatilite simulee
res = []
for i in range(1000):
    path, dt = geom_brownian_path(S0, R, SIGMA, int(T*365), 1, 3)
    res.append(np.log(path[-1]/S0)**2)
np.sqrt(np.mean(res))


# states_df = pd.DataFrame(states)
# states_df.columns = call_hedger_columns()
# states_df["CallPrice-Repli"] = states_df["CallPrice"] - states_df["PnL"]
# px.line(states_df).show()

# px.line(states_df["PnL"] - states_df["CallPrice"]).show()

# res = []
# for i in range(200):
#     if i % 100 == 0:
#         print(i)
#     path, dt = geom_brownian_path(S0, R, SIGMA, int(T*365), 1)
#     states = call_hedger(SIGMA, K, T, R, STEP, path, dt)
#     res.append(states[-1][4]-states[-1][5])

# np.mean(res)

# px.histogram(res).show()
# # px.line(path).show()

# bs.call_delta(SIGMA, K, T, R, 100) * 100
# bs.call_price(SIGMA, K, T, R, 100)
# np.mean(res)


# states_df.columns = bs.callj
