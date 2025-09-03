# fetcher.py
import pandas as pd
import requests
import asyncio
import nest_asyncio
from collections import deque

nest_asyncio.apply()

ohlc_buffer = deque(maxlen=60)
meta_buffer = deque(maxlen=60)
realtime_df_combined = pd.DataFrame()

async def fetch_ohlc_coingecko():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=1"
        response = requests.get(url)
        if response.status_code == 200:
            ohlc_data = response.json()[-10:]
            for o in ohlc_data:
                ts = pd.to_datetime(o[0], unit='ms', utc=True)
                ohlc_buffer.append({
                    "timestamp": ts,
                    "open": o[1],
                    "high": o[2],
                    "low": o[3],
                    "close": o[4]
                })
    except Exception as e:
        print("🔴 OHLC Error:", e)

async def fetch_meta_coingecko():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin"
        res = requests.get(url).json()
        timestamp = pd.to_datetime(res['last_updated'], utc=True)
        market_cap = res['market_data']['market_cap']['usd']
        total_volume = res['market_data']['total_volume']['usd']
        meta_buffer.append({
            "timestamp": timestamp,
            "market_cap": market_cap,
            "total_volume": total_volume
        })
    except Exception as e:
        print("🔴 Meta Error:", e)

async def coingecko_ohlc_loop():
    while True:
        await fetch_ohlc_coingecko()
        await asyncio.sleep(60)

async def coingecko_meta_loop():
    while True:
        await fetch_meta_coingecko()
        await asyncio.sleep(60)

async def main_loop():
    await asyncio.gather(
        coingecko_ohlc_loop(),
        coingecko_meta_loop()
    )

def combine_buffers_to_df():
    global realtime_df_combined

    if ohlc_buffer and meta_buffer:
        try:
            df_ohlc = pd.DataFrame(list(ohlc_buffer))
            df_meta = pd.DataFrame(list(meta_buffer))

            for df in [df_ohlc, df_meta]:
                df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
                df.drop_duplicates(subset='timestamp', keep='last', inplace=True)

            df_ohlc.sort_values('timestamp', inplace=True)
            df_meta.sort_values('timestamp', inplace=True)

            df_merge = pd.merge_asof(
                df_ohlc, df_meta, on='timestamp',
                direction='backward', tolerance=pd.Timedelta('2min')
            )

            df_merge.set_index('timestamp', inplace=True)
            realtime_df_combined = df_merge.dropna()
        except Exception as e:
            print(f"❌ Combine Error: {e}")