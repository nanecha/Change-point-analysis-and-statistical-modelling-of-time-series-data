# Brent Oil Price Analysis: Task 1 - Laying the Foundation

This project sets the groundwork for analyzing how geopolitical events, economic indicators, and policy decisions impact **Brent Crude Oil Prices**. The focus of **Task 1** is to perform an initial exploration, data cleaning, and visualization of the Brent oil price time series data.

---

## 📁 Folder Structure

```
Change-point-analysis-and-statistical-modelling-of-time-series-data/
├── data/
│   └── BrentOilPrices.csv
├──github
│   └──workflows
│      └──ci.yml
├── notebooks/
│   └── data_preprocessing.ipynb
├── src/
│   └── data_eda.py  # Modular analysis functions
│   └──__init__.py
├── README.md
├── requirements.txt
├──.gitignore
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone 
cd brent-oil-analysis
```

2. **Create virtual environment & activate**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 📦 Dependencies (in `requirements.txt`)

```
pandas
matplotlib
seaborn
```

---

## 🚀 Use Case & Task Overview

This task includes the following steps:

### ✅ Data Loading & Initial Inspection

```python
from src.data_eda import load_data, preview_data, show_info, show_shape

df = load_data('data/BrentOilPrices.csv')
preview_data(df)
show_info(df)
show_shape(df)
```

### ✅ Statistical Summary

```python
from src.data_analysis import summarize_data
print(summarize_data(df))
```

### ✅ Data Quality Checks

```python
from src.data_eda import check_missing_values, check_duplicates
print(check_missing_values(df))
print(check_duplicates(df))
```

### ✅ Data Visualization

```python
from src.data_analysis import plot_brent_prices
plot_brent_prices(df)
```

---

## 🔍 Purpose of This Task

* Establish a **clean and understandable dataset**
* Visualize price **trends and volatility**
* Prepare for deeper statistical modeling and event-based impact analysis in the next tasks

---

## 🧠 Next Steps

* Time series modeling (ARIMA, Change Point Detection)
* Feature engineering for geopolitical events
* Causal analysis between events and price changes

---

## 📄 References

* [Data Science Workflow](https://www.datascience-pm.com/data-science-workflow/)
* [Mastering the Data Science Workflow](https://towardsdatascience.com/mastering-the-data-science-workflow-2a47d8b613c4)
