##app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)
DATA_DIR = Path('F:/Change-point-analysis-and-statistical-modelling-of-time-series-data/data')

# --- Utilities ---------------------------------------------------------------


def load_prices():
    p = DATA_DIR / 'BrentOilPrices.csv'
    df = pd.read_csv(p, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)
    return df


def load_forecast():
    p = DATA_DIR / 'change_point_results.csv'
    if p.exists():
        df = pd.read_csv(p, parse_dates=['date']).sort_values('date').reset_index(drop=True)
        return df
    return pd.DataFrame(columns=['date', 'forecast'])


def load_events():
    p = DATA_DIR / 'event.csv'
    df = pd.read_csv(p, parse_dates=['date']).sort_values('date').reset_index(drop=True)
    return df

# --- Filters -----------------------------------------------------------------

def apply_date_filter(df: pd.DataFrame, start: str | None, end: str | None, col: str = 'date'):
    if start:
        df = df[df[col] >= pd.to_datetime(start)]
    if end:
        df = df[df[col] <= pd.to_datetime(end)]
    return df

# --- API Endpoints -----------------------------------------------------------

@app.get('/api/health')
def health():
    return {'status': 'ok'}

@app.get('/api/prices')
def api_prices():
    start = request.args.get('start')
    end = request.args.get('end')
    window = int(request.args.get('roll', 0))  # rolling mean window (days)

    df = load_prices()
    df = apply_date_filter(df, start, end)
    if window and window > 1:
        df['price_smooth'] = df['price'].rolling(window, min_periods=1).mean()

    return jsonify(df.assign(date=df['date'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'))

@app.get('/api/forecast')
def api_forecast():
    start = request.args.get('start')
    end = request.args.get('end')

    df = load_forecast()
    df = apply_date_filter(df, start, end)
    return jsonify(df.assign(date=df['date'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'))

@app.get('/api/events')
def api_events():
    start = request.args.get('start')
    end = request.args.get('end')
    event_type = request.args.get('type')  # optional filter

    df = load_events()
    if event_type:
        df = df[df['event_type'] == event_type]
    df = apply_date_filter(df, start, end)

    return jsonify(df.assign(date=df['date'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'))

@app.get('/api/metrics')
def api_metrics():
    """Return basic indicators: volatility, avg move around events."""
    lookback = int(request.args.get('lookback', 30))  # days for volatility
    window = int(request.args.get('event_window', 3))  # days before/after

    prices = load_prices().copy()
    prices['ret'] = prices['price'].pct_change()

    # Simple annualized volatility based on last N days
    if lookback > 1:
        vol = prices['ret'].tail(lookback).std() * (252 ** 0.5) if len(prices) >= 2 else None
    else:
        vol = prices['ret'].std() * (252 ** 0.5) if len(prices) >= 2 else None

    # Average move around events
    events = load_events()
    out = []
    for _, row in events.iterrows():
        d = row['date']
        mask = (prices['date'] >= d - pd.Timedelta(days=window)) & (prices['date'] <= d + pd.Timedelta(days=window))
        seg = prices.loc[mask].copy()
        if seg.empty:
            continue
        baseline = prices.loc[prices['date'] < d].tail(1)['price']
        after = prices.loc[prices['date'] >= d].head(1)['price']
        delta = None
        if len(baseline) and len(after):
            delta = float((after.values[0] - baseline.values[0]) / baseline.values[0])
        out.append({
            'date': d.strftime('%Y-%m-%d'),
            'title': row.get('title', ''),
            'event_type': row.get('event_type', ''),
            'avg_window_price': float(seg['price'].mean()) if 'price' in seg else None,
            'event_delta': delta  # immediate relative change at event date
        })

    metrics = {
        'annualized_volatility': vol,
        'event_impacts': out,
        'counts': {
            'prices': int(len(prices)),
            'events': int(len(events))
        }
    }
    return jsonify(metrics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)