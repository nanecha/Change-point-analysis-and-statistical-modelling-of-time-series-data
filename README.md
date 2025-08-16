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

* Time series modeling ( Change Point Detection)
* Feature engineering for geopolitical events
* Causal analysis between events and price changes

---

## 📄 References

* [Data Science Workflow](https://www.datascience-pm.com/data-science-workflow/)
* [Mastering the Data Science Workflow](https://towardsdatascience.com/mastering-the-data-science-workflow-2a47d8b613c4)


# Brent Oil Price Analysis and Visualization Project

## Overview
This project analyzes historical Brent oil price data (2011–2025) to identify significant price changes, associate them with geopolitical and economic events, and present findings through an interactive web-based dashboard. The project is divided into three tasks:

- **Task 1**: Compile a dataset of events impacting Brent oil prices and perform exploratory data analysis (EDA).
- **Task 2**: Apply a Bayesian change point model to detect significant price shifts and correlate them with events.
- **Task 3**: Develop a Flask (backend) and Vite-React (frontend) dashboard to visualize price trends, events, change points, and key indicators.

The project uses Python (`pandas`, `numpy`, `pymc`, `arviz`, `matplotlib`, `seaborn`, `flask`) for data analysis and backend, and JavaScript (`react`, `recharts`, `tailwindcss`, `vite`) for the frontend. The dashboard features a line chart with event and change point markers, date range filters, a clickable event table, key indicators (volatility, price change), and responsive design.

## Project Structure
brent_dashboard/
├── api.py                  # Flask API endpoints for prices, events, change points
├── app.py                  # Flask app serving Vite build
├── brent_oil_prices.csv    # Historical Brent oil price data (Date, Price)
├── change_point_results.csv # Output from Task 2 (change point data)
├── brent_change_point.png  # Plot from Task 2 (price series with change points)
├── src/                    # Vite project root
│   ├── src/                # React source files
│   │   ├── main.jsx        # React entry point
│   │   ├── App.jsx         # Dashboard component
│   │   ├── index.css       # Tailwind CSS
│   │   └── assets/         # Static assets (if needed)
│   ├── public/             # Vite public assets
│   │   ├── index.html      # Vite entry HTML
│   │   └── vite.svg        # Favicon
│   ├── vite.config.js      # Vite configuration
│   ├── package.json        # Node.js dependencies
│   ├── tailwind.config.js  # Tailwind configuration
│   └── dist/               # Vite build output (generated)
├── static/                 # Flask static folder for Vite build
└── README.md               # Project documentation
text## Prerequisites
- **Python 3.8+**: For backend and analysis.
- **Node.js 16+**: For frontend development and build.
- **Dependencies**:
  - Python: `flask`, `pandas`, `numpy`, `pymc`, `arviz`, `matplotlib`, `seaborn`
  - Node.js: `react`, `react-dom`, `recharts`, `vite`, `@vitejs/plugin-react`, `tailwindcss`, `postcss`, `autoprefixer`

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd brent_dashboard
2. Set Up Python Environment
bash# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install flask pandas numpy pymc arviz matplotlib seaborn
3. Set Up Node.js Environment
bashcd src
npm install
4. Prepare Data

Ensure brent_oil_prices.csv is in brent_dashboard/ with columns:

Date (YYYY-MM-DD)
Price (USD/bbl)


The project assumes a 2011–2025 dataset. Adjust api.py if column names or date formats differ:
pythonprice_data = price_data.rename(columns={'date': 'Date', 'price': 'Brent_Price'})
price_data['Date'] = pd.to_datetime(price_data['Date'], format='%d-%m-%Y')  # Adjust format


Usage
Task 1: Event Dataset and EDA

Objective: Compile a dataset of geopolitical/economic events and perform EDA.
Implementation:

Event dataset (12 events, e.g., Russia-Ukraine War, OPEC+ Production Cuts) is defined in api.py.
EDA is performed in src/brent_change_point_analysis.py using exploratory_analysis() to visualize price trends and event correlations.


Run:
bashpython src/brent_change_point_analysis.py

Output:

Visualizations of price trends with event markers.
Summary statistics (mean, volatility) printed to console.

Task 2: Bayesian Change Point Analysis

Objective: Detect significant price change points and associate them with events.
Implementation:

Uses pymc to model a single change point with two normal distributions for prices before and after (bayesian_change_point_model()).
Interprets results (interpret_model()) to extract change point date, mean prices, and associated events.
Saves results to change_point_results.csv and generates brent_change_point.png.

Code (from provided Task 2):
pythonprice_data, event_data = load_and_prepare_data()
exploratory_analysis(price_data, event_data)


Run:
bashpython src/brent_change_point_analysis.py

Output:

change_point_results.csv: Change point dates, mean prices, and associated events.
brent_change_point.png: Plot of price series with change points and events.

Note: Assumes sufficient data (2011–2025). Short datasets (e.g., 10 days) may cause errors; use a longer time series for reliable detection.

Task 3: Interactive Dashboard

Objective: Develop a Flask and Vite-React dashboard to visualize price trends, events, and change points.
Implementation:

Backend (Flask):

api.py: Defines /api/prices, /api/events, /api/change_points endpoints to serve data.
app.py: Serves Vite-built static/index.html and assets.

Frontend (Vite-React):

Located in src/ with src/main.jsx, src/App.jsx, src/index.css.
Uses recharts for line charts, tailwindcss for styling.
Features:

Line chart with price trends, red event markers, green change point markers.
Date range filters for data selection.
Clickable event table for highlighting.
Key indicators: max volatility, average price change.
Responsive design for desktop, tablet, mobile.

Run:

Build the frontend:
bashcd src
npm run build
This generates brent_dashboard/static/ with index.html and assets.
Run the Flask backend:
bashcd ..
python app.py
Access at http://127.0.0.1:5000.
For development with hot reloading:
bashcd src
npm run dev
Run Flask in another terminal, then access at http://localhost:5173.


Output:

Interactive dashboard with visualizations and filters.
Example indicators: Max volatility (e.g., 5.23%), average price change (e.g., 30.44%).

Troubleshooting

Data Issues:

Ensure brent_oil_prices.csv is in brent_dashboard/ with correct columns.
Update api.py for different column names or date formats:
pythonprice_data = price_data.rename(columns={'date': 'Date', 'price': 'Brent_Price'})
price_data['Date'] = pd.to_datetime(price_data['Date'], format='%d-%m-%Y')

Vite Build Errors:

Verify src/public/index.html and src/src/main.jsx exist.
Clear node_modules and rebuild:
bashcd src
rmdir /s /q node_modules
del package-lock.json
npm install
npm run build

Future Enhancements

Integrate real-time Brent price data via an EIA API in api.py.
Add multiple change point detection in Task 2 using advanced models (e.g., Markov-Switching).
Enhance dashboard with zoomable charts (Recharts brush) and CSV export.
Deploy to a cloud platform (e.g., Heroku, AWS) with Gunicorn.

