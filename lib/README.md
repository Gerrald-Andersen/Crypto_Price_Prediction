# 📁 `lib/` — Model, Pipeline, and Scaling Utilities

This folder contains the trained LSTM model, preprocessing pipelines, and scaling utilities used in the Bitcoin price prediction dashboard. These components are loaded by the Streamlit app and serve as the backend for real-time forecasting.

---

## 📦 Contents

| File / Folder              | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| `lstm_model.keras`        | Trained LSTM model for predicting future BTC prices                     |
| `lstm_best_params.pkl`    | Serialized dictionary of best hyperparameters used during model tuning  |
| `scaler_pipeline.pkl`     | Preprocessing pipeline for scaling time series input features           |
| `timeseries_scaler.py`    | Custom scaler class for transforming multivariate time series data      |

---

## 🧠 Usage Notes

- The `.keras` model is loaded using `tensorflow.keras.models.load_model()` with `compile=False`.
- The `.pkl` files are loaded using `pickle.load()` and contain either preprocessing logic or model parameters.
- `timeseries_scaler.py` defines a reusable class for scaling sequences and reshaping input for LSTM models.
- These files are not meant to be executed directly, but imported and used by the main dashboard (`main.py`).

---

## ⚖️ License

This project is proprietary. All rights reserved © 2025 Gerrald Andersen.  
No part of this repository may be copied, modified, reused, or redistributed without explicit written permission.

![License: Proprietary](https://img.shields.io/badge/license-Proprietary-red.svg)
