# 📁 `src/` — Core Modules for Bitcoin Price Prediction

This folder contains the core components of the Bitcoin price prediction pipeline, from data acquisition to LSTM model training. All modules are designed to integrate with the Streamlit dashboard and support real-time data updates.

---

## 📦 Module Structure

| File / Folder                             | Purpose                                                                 |
|-------------------------------------------|-------------------------------------------------------------------------|
| `Fetch_Historical_Data.ipynb`             | Fetches OHLC, volume, and market cap data from the CoinGecko API        |
| `Feature_Engineering.ipynb`               | Computes technical indicators such as VWAP and VPT                      |
| `LSTM_Model.ipynb`                        | Builds and trains the LSTM model for BTC price prediction               |

---

## 🔄 Execution Flow

1. **`Fetch_Historical_Data.ipynb`**  
   Retrieves real-time data from CoinGecko and stores it as a DataFrame.

2. **`Feature_Engineering.ipynb`**  
   Adds technical features like VWAP and VPT to the raw data.

4. **`LSTM_Model.ipynb`**  
   Trains the LSTM model and saves it as a `.keras` file.

---

## 🧠 Usage Notes

- All modules are designed to be modular and testable in isolation.
- Follow the pipeline order: `fetch → feature → scale → predict`.
- The trained model and scaler pipeline are stored in the `lib/` folder for dashboard integration.

---

## ⚖️ License

This project is licensed under the **Apache License 2.0**.  
See the [`LICENSE`](../LICENSE) file for full details.
