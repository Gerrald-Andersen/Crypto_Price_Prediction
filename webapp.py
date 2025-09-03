# ============================================
# 📈 Streamlit Dashboard for Bitcoin Price Prediction
# ============================================

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh
import pickle
from tensorflow.keras.models import load_model
import numpy as np
from timeseries_scaler import TimeSeriesScaler
import os

# ------------------ Configuration ------------------
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
st.set_page_config(page_title="📈 Bitcoin Price Realtime", layout="centered")
st.title("📊 Realtime Bitcoin Price Visualization (CoinGecko API)")
st.markdown("🔁 Auto-refresh every 30 minutes + manual refresh button")
st.divider()

# ------------------ Session State Timer ------------------
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = 0

cooldown = 300  # 5 minutes
time_since = time.time() - st.session_state.last_refresh
refresh = False

countdown_placeholder = st.empty()
progress_bar = st.progress(0)

if time_since < cooldown:
    remaining = int(cooldown - time_since)
    minutes, seconds = divmod(remaining, 60)
    countdown_placeholder.markdown(
        f"<div style='padding:10px; border-radius:8px; background-color:#222;'>"
        f"<span style='color:#f0c929; font-weight:bold;'>⏳ Please wait {minutes:02d}:{seconds:02d}</span> "
        f"<span style='color:#aaa;'>before manual refresh is available again.</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    progress_bar.progress((cooldown - remaining) / cooldown)
else:
    if st.button("🔄 Refresh Now"):
        st.session_state.last_refresh = time.time()
        refresh = True

# ------------------ Prediction State Initialization ------------------
if "predicted_price" not in st.session_state:
    st.session_state.predicted_price = None
    st.session_state.prediction_time = 0

# ------------------ Conditional Auto-refresh ------------------
prediction_interval = 1800  # 30 minutes
time_since_prediction = time.time() - st.session_state.prediction_time

if st.session_state.predicted_price is None or time_since_prediction > prediction_interval:
    st_autorefresh(interval=30 * 60 * 1000, key="refresh_30min")
    st_autorefresh(interval=1000, key="countdown_tick")
else:
    st.info("✅ Prediction is available. Auto-refresh is temporarily disabled until the next 30-minute cycle.")

# ------------------ Data Fetching ------------------
@st.cache_data(ttl=1800)
def fetch_btc_ohlc():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=1"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms").dt.tz_localize('UTC')
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)
    return df

@st.cache_data(ttl=600)
def fetch_market_cap():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true"
    response = requests.get(url)
    data = response.json()
    df_mc = pd.DataFrame.from_dict({
        "timestamp": [datetime.now(timezone.utc)],
        "market_cap": [data["bitcoin"]["usd_market_cap"]]
    })
    df_mc.set_index("timestamp", inplace=True)
    return df_mc

@st.cache_data(ttl=1800)
def fetch_volume_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"
    response = requests.get(url)
    data = response.json()
    volume_data = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
    volume_data["timestamp"] = pd.to_datetime(volume_data["timestamp"], unit="ms").dt.tz_localize('UTC')
    volume_data.set_index("timestamp", inplace=True)
    return volume_data

# ------------------ Manual or Automatic Refresh ------------------
if refresh:
    with st.spinner("🔄 Fetching new data..."):
        try:
            df = fetch_btc_ohlc.__wrapped__()
            market_cap = fetch_market_cap.__wrapped__()
            volume_df = fetch_volume_data.__wrapped__()
        except Exception as e:
            st.error(f"Manual refresh failed: {e}")
            st.stop()
else:
    df = fetch_btc_ohlc()
    market_cap = fetch_market_cap()
    volume_df = fetch_volume_data()

# ------------------ Merge OHLC and Volume ------------------
volume_df_resampled = volume_df.resample("5min").mean()
df_graphic = df.join(volume_df_resampled, how="left")

df_graphic["vwap"] = ((df_graphic["high"] + df_graphic["low"] + df_graphic["close"]) / 3 * df_graphic["volume"]).cumsum() / df_graphic["volume"].cumsum()
df_graphic["vpt"] = (df_graphic["volume"] * df_graphic["close"].pct_change()).cumsum()

df_table = df_graphic.copy()
df_predict = df.copy()
df_predict["market_cap"] = market_cap["market_cap"].iloc[-1]

# ------------------ Load Model and Pipeline ------------------
try:
    model = load_model("lstm_model.keras", compile=False)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

try:
    with open("scaler_pipeline.pkl", "rb") as f:
        pipeline = pickle.load(f)
except Exception as e:
    st.error(f"Failed to load pipeline: {e}")
    st.stop()

# ------------------ Price Prediction ------------------
MAX_SEQ_LEN = 48
features = df_predict.columns
actual_len = len(df_predict)

if st.session_state.predicted_price is None or time_since_prediction > prediction_interval:
    with st.spinner("⏳ Please wait, generating prediction..."):
        if actual_len >= 1:
            last_seq = df_predict.iloc[-actual_len:].values.reshape(1, actual_len, df_predict.shape[1])

            if actual_len < MAX_SEQ_LEN:
                pad_width = MAX_SEQ_LEN - actual_len
                pad_array = np.zeros((1, pad_width, df_predict.shape[1]))
                last_seq = np.concatenate([pad_array, last_seq], axis=1)

            if last_seq.shape[1:] != model.input_shape[1:]:
                st.warning("⚠️ Data shape mismatch for prediction.")
            else:
                try:
                    X_scaled = pipeline.transform(last_seq)
                    prediction = model.predict(X_scaled)
                    st.session_state.predicted_price = prediction[0][0]
                    st.session_state.prediction_time = time.time()
                except Exception:
                    st.warning("⚠️ Prediction failed. Please try manual refresh.")
        else:
            st.warning("⚠️ Not enough data for prediction.")
else:
    st.caption("✅ Prediction already available and not recalculated.")

# ------------------ Display Prediction ------------------
if st.session_state.predicted_price is not None:
    st.metric("🔮 Next Predicted BTC Price", f"${st.session_state.predicted_price:,.2f}")
    df_table["Predicted Price"] = st.session_state.predicted_price
else:
    df_table["Predicted Price"] = 'error'

# ------------------ Display UTC Time ------------------
utc_now = datetime.now(timezone.utc)
st.write(f"*Current UTC Time:* :blue-badge[{utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}]")

# ------------------ Display Latest Data ------------------
if df.empty:
    st.warning("⚠️ Data is empty or failed to load.")
    st.stop()

last_price = df["close"].iloc[-1]

col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Latest BTC Price (USD)", f"${last_price:,.2f}")
with col2:
    st.metric("🏦 BTC Market Cap (USD)", f"${market_cap['market_cap'].iloc[-1]:,.0f}")

# ------------------ Price & VWAP Chart ------------------
st.write("### 📉 BTC Price & VWAP Chart")
st.line_chart(df_graphic[["close", "vwap"]].tail(100))

# ------------------ VPT Chart ------------------
st.write("### 🔁 Volume Price Trend (VPT) Chart")
st.line_chart(df_graphic["vpt"].tail(100))

# ------------------ Full Data Table ------------------
with st.expander("📋 View Full Data (Last 10 + Market Cap + Predicted Price)"):
    df_tail = df_table.tail(10).copy()
    st.dataframe(df_tail, use_container_width=True)