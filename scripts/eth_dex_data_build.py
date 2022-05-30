import os
import numpy as np
import pandas as pd
import src.colnames as n
import matplotlib.pyplot as plt

# This script aims to extend arbitrum eth data extracted from the graph
# main work is about block time. 1/ request some datetime for a sublist
# of blocks, 2/ then interpolate datetime for the remaining blocks.

DATA_DIR = None  # YOUR DATA DIR HERE

if not DATA_DIR:
    print("Please provide a DATA_DIR to read arbitrum eth block prices")
    exit

# read Arbitrum ETH 5 prices
filepath = os.path.join(DATA_DIR, "Data_Arb_ETH_USDC_5_227484.csv")
df = pd.read_csv(filepath)
df[n.Price] = df["amount1"].abs() / df["amount0"].abs()
df = df[["transaction_hash", "block_number", n.Price, "sqrt_price_x96"]]
df.columns = [n.TxHash, n.Block, n.Price, n.Spot]

# read Arbitrun block times
filepath = os.path.join(DATA_DIR, "arbitrum_block_times.csv")
bdf = pd.read_csv(filepath)
bdf.columns = [n.Block, n.Date]
bdf = bdf.sort_values(n.Block)
bdf[n.Date] = pd.to_datetime(bdf[n.Date])
cdf = bdf.diff(axis=0)
bdf[n.BlockTime] = cdf[n.Date].apply(
    lambda x: x.total_seconds()) / cdf[n.Block]

# merge and work on block times
df.set_index(n.Block, inplace=True)
bdf.set_index(n.Block, inplace=True)
ndf = df.join(bdf)

# propagate missing data
ndf[n.BlockTime] = ndf[n.BlockTime].bfill().ffill()
ndf[n.Date] = ndf[n.Date].ffill().bfill()


def compute_date_spot(gdf):
    """
    function to be applied for a single date,
    in order to interpolate block date from average block time
    and first date
    """

    # gdf = ndf.loc[ndf[n.Date] == ndf[n.Date].iloc[0]]
    nBlockDelta = "BlockDelta"
    gdf[nBlockDelta] = np.diff(gdf.index.to_numpy(), prepend=np.nan)

    nCumSecsDelta = "CumSecsDelta"
    gdf[nCumSecsDelta] = (
        gdf[n.BlockTime] * gdf[nBlockDelta]).cumsum().fillna(0)

    nDateSpot = "DateSpot"
    gdf[nDateSpot] = gdf[n.Date]

    return (gdf[n.Date] + pd.to_timedelta(gdf[nCumSecsDelta], unit='s'))


# compute imterpolated BlockDate
nBlockDate = "BlockDate"
block_date = ndf.groupby(n.Date, group_keys=False).apply(
    compute_date_spot).astype('datetime64[s]')
block_date.name = nBlockDate

rdf = ndf.join(block_date).reset_index()
rdf = rdf[[nBlockDate, n.Price, n.Spot]]
rdf.columns = [n.Date, n.Price, n.Spot]

# rdf.to_csv("2021-08-31_2022-04-01_eth_arbitrum.csv", index=False)

# plotting price/spot
pdf = rdf.iloc[500:]
plt.plot(pdf[n.Date], pdf[n.Spot])
plt.show()


# # Downloading ARBISCAN block time
# #
#
# file = open("arbitrum_block_time.csv", "a")
#
# for b in blocks.to_numpy():
#     if b in df[n.Block]:
#         print("{0} not downloaded".format(b))
#         continue
#     d = arb.get_block_time(b)
#     print("{block},{date}".format(block=b, date=d.isoformat()))
#     file.write("{block},{date}\n".format(block=b, date=d.isoformat()))
#     time.sleep(5)
#
# file.close()
