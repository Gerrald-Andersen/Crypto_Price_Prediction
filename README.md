# 📈 Crypto Price Prediction Dashboard

## 🧭 Purpose

This application was developed to assist cryptocurrency traders—particularly Bitcoin enthusiasts—in making more informed trading decisions. By providing real-time price visualization and predictive insights, the dashboard aims to help users anticipate market movements and minimize potential losses. While not a substitute for financial advice, it offers a data-driven perspective that can complement trading strategies.

---

## ⚙️ What I Did

The development process involved several key stages:
1. **Task Plan**
   - Before initiating the project, I carefully outlined a task plan to ensure clarity, focus, and efficiency throughout the development process. The goal was to build a predictive dashboard that could assist crypto traders in making smarter decisions.

2. **Data Collection**  
   - Fetched real-time Bitcoin market data from the [CoinGecko API](https://www.coingecko.com/en/api), including OHLC (Open, High, Low, Close), volume, and market capitalization.

3. **Feature Engineering**  
   - Processed raw data and created additional indicators such as VWAP (Volume Weighted Average Price) and VPT (Volume Price Trend) to enrich the dataset.

4. **Model Development**  
   - Built a Long Short-Term Memory (LSTM) deep learning model to predict future Bitcoin prices based on historical patterns.
   - Hyperparameter tuning was deferred due to computational cost constraints.

5. **Web Application Deployment**  
   - Developed an interactive dashboard using [Streamlit](https://streamlit.io/) to visualize price trends, display predictions, and allow real-time interaction with the data.

---

## 📊 Results

Although the LSTM model does not yet produce highly accurate predictions, the project successfully demonstrates the integration of deep learning with live crypto data. More importantly, it has been a rich learning experience, allowing me to explore:

- Time series modeling
- API integration and data pipelines
- Feature engineering for financial data
- Streamlit-based UI development
- Model deployment and performance monitoring

The dashboard provides a functional base that can be expanded and refined over time.

---

## 🚀 Future Improvements

Planned enhancements include:

- **Model Tuning**  
  - Apply hyperparameter optimization and cross-validation to improve prediction accuracy.

- **Expanded Feature Set**  
  - Integrate additional technical indicators (e.g., RSI, MACD) and external signals such as sentiment analysis.

- **Multi-Currency Support**  
  - Extend the dashboard to support other cryptocurrencies beyond Bitcoin.

- **Cloud Deployment**  
  - Host the application on a scalable cloud platform for broader accessibility and real-time performance.
