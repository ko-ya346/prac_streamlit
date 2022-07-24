import numpy as np

import streamlit as st
import pandas as pd

import plotly.graph_objects as go

# google drive上のcsvファイルのURL
URL = (
    "https://drive.google.com/file/d/1Q2c6pRbZp16tzGUFLB9X-I_7IJcROxUW/view?usp=sharing"
)
# google drive api key
KEY = st.secrets.GoogleDriveApiKey.key
DEBUG = True


@st.cache
def load_data(debug):
    """
    Args:
        url: google drive
    """
    path = f"https://www.googleapis.com/drive/v3/files/{URL.split('/')[-2]}?alt=media&key={KEY}"
    df = pd.read_csv(path)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")

    if debug:
        df = df.iloc[-10000:].reset_index(drop=True)

    return df


def trunc_timestamp(df, freq, timestamp_col="Timestamp"):
    if freq == "1month":
        df[timestamp_col] = df[timestamp_col].dt.to_period("M").dt.to_timestamp()
    elif freq == "1week":
        df[timestamp_col] = df[timestamp_col].dt.floor("7D")
    elif freq == "1day":
        df[timestamp_col] = df[timestamp_col].dt.floor("d")
    elif freq == "4hour":
        hours4_to_seconds = 4 * 60 * 60
        df[timestamp_col] = pd.to_datetime(
            df[timestamp_col].map(lambda x: x.timestamp())
            // hours4_to_seconds
            * hours4_to_seconds,
            unit="s",
        )
    elif freq == "30min":
        df[timestamp_col] = df[timestamp_col].dt.floor("30T")
    else:
        df[timestamp_col] = df[timestamp_col].dt.floor("15T")
    return df


# cacheした変数をいじるとwarningでる
org_df = load_data(debug=DEBUG)
df = org_df.copy(deep=True)

# sliderで表示期間を指定
ymd = df["Timestamp"].dt.floor("d").unique()
from_ymd, to_ymd = st.sidebar.select_slider(
    "Select the period for displaying candlesticks.",
    options=ymd,
    value=(np.min(ymd), np.max(ymd)),
)
cond1 = df["Timestamp"] >= from_ymd
cond2 = df["Timestamp"] <= to_ymd
df = df[cond1 & cond2].reset_index(drop=True)
st.write(df.head())

# 時間足を選択
freq_lst = ["1month", "1week", "1day", "4hour", "1hour", "30min", "15min"]
freq = st.selectbox("Select freq", freq_lst)
df = trunc_timestamp(df, freq, "Timestamp")

# ローソク足生成
candle_df = (
    df.groupby("Timestamp")
    .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"})
    .reset_index()
)

pl = st.empty()
pl.text("Now drawing plots")
fig = go.Figure()
fig.add_trace(
    go.Candlestick(
        x=candle_df["Timestamp"],
        open=candle_df["Open"],
        high=candle_df["High"],
        low=candle_df["Low"],
        close=candle_df["Close"],
    )
)
pl.plotly_chart(fig)

# candle, 折れ線グラフ両方だす
# 折れ線グラフは列名を選択
