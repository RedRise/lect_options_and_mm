import os
import pandas as pd
import src .colnames as n

nasdaq_com_names = ["Date", "C", "V", "O", "H", "L"]


def read_csv_nasdaq_com(filepath: str) -> pd.DataFrame:
    # filepath = os.path.join("data", "market", "2017-05-23_2022-05-20_SPX_nasdaq_com.csv")

    df = pd.read_csv(filepath)
    df["Date"] = pd.to_datetime(df["Date"])
    df.columns = nasdaq_com_names

    return df


def read_csv_eth_arbitrum(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df[n.Date] = pd.to_datetime(df[n.Date]).astype("datetime64[s]")
    return df
