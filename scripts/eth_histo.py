import os
import numpy as np
import pandas as pd
import plotly.express as px
from src.option_hedger import *
import src.black_scholes as bs

filepath = os.path.join("data", "market", "2016-01-01_2022-05-22_ethereumprice_org.csv")

nTimestamp = "timestamp"

nOptionValo = "OptionValo"
nRepliVsOption = "RepliVsOption"

nDate = "Date"
nPrice = "Price"
nHvol = "hv"
nDlog = "dlog"

STD_WIN = 120

df = pd.read_csv(filepath)
df[nDate] = pd.to_datetime(df[nTimestamp], unit='s')
df = df[[nDate, "open"]]
df.columns = [nDate, nPrice]
df = df.set_index(nDate).sort_index()

df[nDlog] = np.log(df[nPrice] / df[nPrice].shift(1))
df[nHvol] = df[nDlog].rolling(STD_WIN).std().multiply(np.sqrt(365)).shift(2)
px.line(df).show()

i = 1180

res = []

for i in range(250, len(df)-365, 30):
    print(i)
    DATE = df.index[i]
    R = 0
    K = S0 = df.iloc[i][nPrice]
    SIGMA = df.iloc[i][nHvol]
    T = 1
    dt = 1/365
    path = df.iloc[i:(i+365)][nPrice].to_list()

    hedges_dlog = np.exp([0.05 * i for i in range(-40,40)])
    states = replicate_call(SIGMA, K, T, R, list(hedges_dlog * S0), 100*dt, path, dt, store=True)
    sdf = pd.DataFrame(states)

    sdf[nOptionValo] = sdf.apply(lambda x: bs.call_price(SIGMA, K, x[nTtm], R, x[nPrice]), axis=1)

    sdf[nOptionValo + "(sigma/2)"] = sdf.apply(lambda x: bs.call_price(SIGMA/2, K, x[nTtm], R, x[nPrice]), axis=1)
    sdf[nOptionValo + "(sigma*2)"] = sdf.apply(lambda x: bs.call_price(SIGMA*2, K, x[nTtm], R, x[nPrice]), axis=1)

    sdf["HedgedOption"] = sdf[nOptionValo] - sdf[nValo]
    
    # px.line(sdf).show()
    summary = (i, DATE, sdf["HedgedOption"].iloc[-1], sdf["HedgedOption"].min(), sdf["HedgedOption"].std())

    res.append(summary)


rdf = pd.DataFrame(res)
rdf.columns = ["index", nDate, "PNL", "min(PNL)", "std(PNL)"]
rdf = rdf.set_index(nDate)
px.line(rdf).show()


sdf[320:340]


px.line(df).show()

df.index.diff().apply(lambda x: x.days)

pd.Series(df.index).diff().apply(lambda x: x.days).describe()