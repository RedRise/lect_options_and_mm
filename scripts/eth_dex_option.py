import os
import numpy as np
import pandas as pd
import src.colnames as n
import src.black_scholes as bs
import src.option_hedger as oh
from datetime import datetime
import matplotlib.pyplot as plt
from src.data_loaders import read_csv_eth_arbitrum

filepath = os.path.join(
    "data", "market", "2021-08-31_2022-04-01_eth_arbitrum.csv")

df = read_csv_eth_arbitrum(filepath)

NB_DAY_PER_YEAR = 365
NB_SECONDS_PER_DAY = 60 * 60 * 24

nDt = "nDt"
df[nDt] = df[n.Date].diff().apply(lambda x: x.total_seconds() /
                                  NB_SECONDS_PER_DAY / NB_DAY_PER_YEAR)

cdf = df.loc[df[n.Date] >= datetime(
    2021, 10, 1)].loc[df[n.Date] <= datetime(2022, 10, 1)]
# plt.plot(cdf[n.Date], cdf[n.Spot])
# plt.show()


R = 0
K = S0 = cdf[n.Spot].iloc[0]
SIGMA = 0.25

T = cdf[n.Date].iloc[[0, -1]].diff().iloc[-1].total_seconds() / \
    NB_SECONDS_PER_DAY / NB_DAY_PER_YEAR
path = cdf[n.Spot]
dt = cdf[nDt]

hedges_dlog = np.exp([5 * i for i in range(-40, 40)])
states = oh.replicate_call(SIGMA, K, T, R, list(
    hedges_dlog * S0), 1/365, path, dt, store=True)

sdf = pd.DataFrame(states)

# sdf[n.Option] = sdf.apply(lambda x: bs.call_price(
#     SIGMA, K, x[n.Ttm], R, x[n.Price]), axis=1)
# sdf[n.OptionHedged] = sdf[n.Option] - sdf[n.Valo]


for col in [n.LimAsk, n.Price, n.LimBid]:
    plt.plot(sdf.index, sdf[col], label=col)

plt.legend()
plt.show()

bs.call_price(SIGMA, K, T, R, K)
sdf
