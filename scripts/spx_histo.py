import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.option_hedger import *
import src.black_scholes as bs
import src.data_loaders as dl
import src.colnames as n
import src.plot_utils as pl

STD_WIN = 120

# read historical SPX data
filepath = os.path.join(
    "data", "market", "2017-05-23_2022-05-20_SPX_nasdaq_com.csv")
df = dl.read_csv_nasdaq_com(filepath)
df = df[[n.Date, "C"]]
df.columns = [n.Date, n.Price]
df = df.set_index(n.Date).sort_index()

# Compute historical volatility
df[n.Dlog] = np.diff(np.log(df[n.Price].shift(2)), prepend=np.nan)
df[n.Hvol] = df[n.Dlog].rolling(STD_WIN).std().multiply(np.sqrt(365)).shift(2)

# Display SPX and Historical Volatility
fig = pl.new_subplot()
pl.add_serie(fig, df, n.Price)
pl.add_serie(fig, df, n.Dlog, go.Bar, True, False)
pl.add_serie(fig, df, n.Hvol, second_axis=True)
fig.add_vrect(x0="2020-01-02", x1="2020-12-31",
              line_width=0, fillcolor="green", opacity=0.2)
fig.add_vrect(x0="2021-01-02", x1="2021-12-31",
              line_width=0, fillcolor="red", opacity=0.2)
fig.show()


# Hedging a long Call position
R = 0
YEAR = 2020

# Compute option prices and replication portfolio
df_sub = df.loc[df.index.year == 2020]
date_from, date_to = df_sub.iloc[[0, -1]].index

K = S0 = df_sub.iloc[0][n.Price]
SIGMA = df_sub.iloc[0][n.Hvol]
T = (date_to - date_from).days/365
dt = T/len(df_sub)

# hedges_dlog = np.exp([0.05 * i for i in range(-40,40)])
# states = replicate_call(SIGMA, K, T, R, list(hedges_dlog * S0), 100*dt, path, dt, store=True)
states = replicate_call(SIGMA, K, T, R, 0.5, dt,
                        df_sub[n.Price].to_list(), dt=T/len(df_sub), store=True)

sdf = pd.DataFrame(states)
sdf[n.Option] = sdf.apply(lambda x: bs.call_price(
    SIGMA, K, x[n.Ttm], R, x[n.Price]), axis=1)
sdf[n.Gamma] = sdf.apply(lambda x: bs.call_gamma(
    SIGMA, K, x[n.Ttm], R, x[n.Price])*0.5*(x[n.Price]**2), axis=1)
sdf[n.OptionHedged] = sdf[n.Option] - sdf[n.Valo]
sdf[n.Hvol] = df_sub[n.Hvol].to_numpy()
sdf["Over"] = (0.0+(df_sub[n.Dlog].abs() * np.sqrt(365)
               > df_sub[n.Hvol])).to_numpy()

fig = pl.new_subplot()
pl.add_serie(fig, sdf, n.Price, displayed=False)
pl.add_serie(fig, sdf, n.Valo)
pl.add_serie(fig, sdf, n.Option)
pl.add_serie(fig, sdf, n.OptionHedged)
pl.add_serie(fig, sdf, n.Delta, displayed=False, second_axis=True)
pl.add_serie(fig, sdf, n.Gamma, displayed=False, second_axis=True)
pl.add_serie(fig, sdf, n.Cash, displayed=False, second_axis=True)
fig.update_layout(title_text="Study of SPX Call K={0} & SIGMA={1:.0f}% for year {2}.".format(
    int(K), 100*SIGMA, YEAR))
fig.show()

###
res = []

for i in range(250, len(df)-365, 30):
    print(i)
    DATE = df.index[i]
    R = 0
    K = S0 = df.iloc[i][n.Price]
    SIGMA = df.iloc[i][n.Hvol]
    T = 1
    dt = 1/365
    df_sub = df.iloc[i:(i+365)]
    path = df_sub[n.Price].to_list()

    hedges_dlog = np.exp([0.05 * i for i in range(-40, 40)])
    # states = replicate_call(SIGMA, K, T, R, list(hedges_dlog * S0), 100*dt, path, dt, store=True)
    states = replicate_call(SIGMA, K, T, R, 0.5, 1*dt, path, dt, store=True)
    sdf = pd.DataFrame(states)

    sdf[n.Option] = sdf.apply(lambda x: bs.call_price(
        SIGMA, K, x[n.Ttm], R, x[n.Price]), axis=1)
    sdf[n.Gamma] = sdf.apply(lambda x: bs.call_gamma(
        SIGMA, K, x[n.Ttm], R, x[n.Price]), axis=1)

    sdf[n.OptionHedged] = sdf[n.Option] - sdf[n.Valo]

    sdf[n.Hvol] = df_sub[n.Hvol].to_numpy()

    sdf["Over"] = (0.0+(df_sub[n.Dlog].abs() * np.sqrt(365)
                   > df_sub[n.Hvol])).to_numpy()
    px.line(sdf).show()

    # px.line(sdf).show()
    summary = (i, DATE, sdf[nOptionValo].iloc[-1], sdf["HedgedOption"].iloc[-1],
               sdf["HedgedOption"].min(), sdf["HedgedOption"].std())

    res.append(summary)


rdf = pd.DataFrame(res)
rdf.columns = ["index", nDate, "CallPriceAt0", "PNL", "min(PNL)", "std(PNL)"]
rdf = rdf.set_index(nDate)
px.line(rdf).show()


sdf[320:340]


px.line(df).show()

df.index.diff().apply(lambda x: x.days)

pd.Series(df.index).diff().apply(lambda x: x.days).describe()
