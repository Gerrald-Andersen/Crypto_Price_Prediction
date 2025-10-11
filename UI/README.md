# 📁 `UI/` — Streamlit Dashboard for Bitcoin Price Prediction

This folder contains the Streamlit-based web application that visualizes real-time Bitcoin price data and generates short-term predictions using an LSTM model. The dashboard integrates API data, engineered features, and a trained model to deliver an interactive forecasting experience.

---

## 🚀 Features

- **Live OHLC Data** from CoinGecko API
- **Auto-refresh every 30 minutes** + manual refresh with cooldown
- **VWAP & VPT Charts** for technical insight
- **LSTM-based Price Prediction** with scaled time series input
- **Market Cap Integration** for contextual analysis
- **Session State Management** to control refresh and prediction cycles

---

## 📦 Key Components

| Section                      | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `Configuration`             | Sets page title, layout, and disables TensorFlow optimizations              |
| `Session Timer`             | Implements cooldown logic for manual refresh                                |
| `Auto-refresh Logic`        | Uses `streamlit_autorefresh` to trigger updates every 30 minutes            |
| `Data Fetching`             | Pulls OHLC, volume, and market cap data from CoinGecko API                  |
| `Feature Engineering`       | Calculates VWAP and VPT from merged OHLC and volume data                    |
| `Model Loading`             | Loads LSTM model (`.keras`) and scaler pipeline (`.pkl`) from `lib/` folder |
| `Prediction Logic`          | Pads and scales time series input, then generates BTC price prediction      |
| `Visualization`             | Displays metrics, charts, and full data table with predicted price          |

---

## 🔄 Refresh Behavior

- **Manual Refresh**: Available every 5 minutes via button
- **Auto Refresh**: Triggers every 30 minutes using `st_autorefresh`
- **Prediction Cycle**: Recalculates prediction if older than 30 minutes

---

## 📁 Dependencies

- `streamlit`
- `streamlit_autorefresh`
- `tensorflow.keras`
- `pandas`, `numpy`, `requests`, `pickle`

---

## ⚖️ License

This project is proprietary. All rights reserved © 2025 Gerrald Andersen.  
No part of this repository may be copied, modified, reused, or redistributed without explicit written permission.

![License: Proprietary](https://img.shields.io/badge/license-Proprietary-red.svg)
