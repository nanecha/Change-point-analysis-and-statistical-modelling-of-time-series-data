# 🛢️ Task 1: Laying the Foundation for Analysis  
**SHAP-Based Analysis of Brent Oil Prices**

This task outlines the foundational workflow for analyzing the impact of **geopolitical events**, **OPEC policy changes**, **economic sanctions**, and **conflicts** on Brent crude oil prices. The goal is to identify price drivers, model their effects, and generate actionable insights for stakeholders such as investors, policymakers, and energy companies.

---

## 📌 1. Data Analysis Workflow

### 🔍 1.1 Methodology Overview  
A structured data science approach is followed to ensure accurate, interpretable, and impactful results.

### ✅ Steps:

1. **Problem Definition**
   - Understand how global events impact Brent oil prices.
   - Extract insights for prediction and decision-making.

2. **Data Collection**
   - **Brent Price Data**: Historical daily/monthly prices (e.g., EIA, ICE).
   - **Event Data**: Geopolitical events, OPEC decisions, sanctions, and conflicts (e.g., from World Bank, IEA, news archives).
   - **External Variables**: Macroeconomic indicators (e.g., global GDP, oil inventories, USD index).

3. **Data Preprocessing**
   - Handle missing values, outliers, and inconsistencies.
   - Engineer event-based features (e.g., binary flags, lags).
   - Merge datasets with correct time alignment and granularity.

4. **Exploratory Data Analysis (EDA)**
   - Visualize trends, volatility, and statistical summaries.
   - Overlay events with price spikes.
   - Check for seasonality, trends, and structural breaks.

5. **Modeling**
   - **Time Series Models**: ARIMA, SARIMA.
   - **Change Point Detection**: Bayesian, PELT, CUSUM.
   - **Regression & VAR**: Quantify event impacts controlling for external factors.
   - **Machine Learning (Optional)**: Use Random Forests, Gradient Boosting for complex patterns.

6. **Model Evaluation**
   - Use MAE, RMSE, or BIC to assess performance.

7. **Insights & Interpretation**
   - Identify and quantify impact of events on oil prices.
   - Detect structural breaks and link to key events.
   - Provide tailored recommendations for different stakeholders.

8. **Results Communication**
   - Prepare visual reports and interactive dashboards.
   - Present results to investors (risk/return), policymakers (security), and energy companies (logistics).

---

## 📑 1.2 Event Dataset Compilation

A curated dataset of significant global events that potentially influenced Brent oil prices will be compiled. Events include:
- Conflicts (e.g., Russia-Ukraine war)
- OPEC+ decisions on supply cuts
- Major economic sanctions (e.g., on Iran or Venezuela)
- Global demand shifts (e.g., during COVID-19)

The dataset includes:
- **Event name**
- **Date**
- **Category** (Geopolitical, OPEC, Sanctions, Conflict)
- **Estimated impact direction**

---

## 📚 References

- [Data Science Workflow](https://www.datascience-pm.com/data-science-workflow/)
- [Mastering the Data Science Workflow – TDS](https://towardsdatascience.com/mastering-the-data-science-workflow-2a47d8b613c4)
