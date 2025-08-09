# api.py
import pandas as pd
import numpy as np
from datetime import datetime
from flask import jsonify


def load_data():
    """
    Load Brent oil price data from CSV and event data, compute volatility.
    """
    try:
        # Load historical Brent oil price data from CSV
        price_data = pd.read_csv('F:/Change-point-analysis-and-statistical-modelling-of-time-series-data/data/BrentOilPrices.csv')
        price_data['Date'] = pd.to_datetime(price_data['Date'])
        price_data = price_data.rename(columns={'Price': 'Brent_Price'})
        price_data.sort_values('Date', inplace=True)
        
        # Compute volatility (3-period rolling standard deviation of percentage change)
        price_data['Volatility'] = price_data['Brent_Price'].pct_change().rolling(window=3).std() * 100
        
        # Event data from Task 1
        event_data = pd.DataFrame({
            'Event_Name': [
                'Russia-Ukraine War', 'US-Iran Nuclear Deal Exit', 'OPEC+ Production Cuts (2020)', 
                'Middle East Conflict (2023)', 'US Sanctions on Russia (2023)', 'Red Sea Shipping Disruptions',
                'OPEC+ Production Increase (2025)', 'US-China Trade Tariffs', 'Israel-Iran Conflict Escalation',
                'Saudi Arabia-Russia Price War', 'Libyan Civil War', 'US Strategic Petroleum Reserve Buy'
            ],
            'Event_Type': [
                'Conflict', 'Sanctions', 'OPEC Policy', 'Conflict', 'Sanctions', 'Geopolitical',
                'OPEC Policy', 'Economic', 'Conflict', 'OPEC Policy', 'Conflict', 'Economic'
            ],
            'Start_Date': [
                '2022-02-24', '2018-05-08', '2020-04-12', '2023-10-07', '2023-07-01', '2023-12-01',
                '2025-06-01', '2025-04-01', '2025-06-13', '2020-03-08', '2011-02-15', '2023-09-01'
            ],
            'Description': [
                'Russian invasion of Ukraine led to a ~30% Brent price spike within 2 weeks.',
                'US withdrawal from Iran nuclear deal reduced Iran’s oil exports by 2.4 mb/d.',
                'OPEC+ agreed to cut production by 9.7 mb/d to stabilize prices post-COVID.',
                'Israel-Hamas conflict raised supply disruption fears, increasing volatility.',
                'Sanctions on Russian oil exports led to a spike in Urals prices.',
                'Attacks on ships in the Red Sea disrupted 1/3 of global seaborne oil trade.',
                'OPEC+ planned to increase production by 411 kb/d, impacting price forecasts.',
                'Tariff announcements led to a Brent price drop to below $60/bbl.',
                'Tensions over Iran’s nuclear program spiked Brent prices to $80/bbl.',
                'Saudi Arabia and Russia failed to agree on cuts, causing a 24% Brent drop.',
                'Conflict disrupted Libyan oil production, impacting global supply.',
                'US announced oil purchases to replenish SPR, affecting price volatility.'
            ]
        })
        event_data['Start_Date'] = pd.to_datetime(event_data['Start_Date'])
        
        # Simulated change point results (replace with Task 2 output if available)
        change_points = pd.DataFrame({
            'Change_Point_Date': ['2022-02-01', '2020-03-01'],
            'Mean_Before': [80.5, 85.2],
            'Mean_After': [110.7, 65.3],
            'Price_Change_Percent': [37.52, -23.36],
            'Associated_Events': ['Russia-Ukraine War', 'Saudi Arabia-Russia Price War']
        })
        change_points['Change_Point_Date'] = pd.to_datetime(change_points['Change_Point_Date'])
        
        return price_data, event_data, change_points
    
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Ensure 'brent_oil_prices.csv' is in the same directory with 'Date' (YYYY-MM-DD) and 'Price' columns.")
        return None, None, None


def register_api_routes(app):
    """Register API routes with the Flask app."""
    @app.route('/api/prices', methods=['GET'])
    def get_prices():
        """API to fetch Brent oil price data."""
        price_data, _, _ = load_data()
        if price_data is None:
            return jsonify({'error': 'Failed to load price data'}), 500
        price_data['Date'] = price_data['Date'].dt.strftime('%Y-%m-%d')
        return jsonify(price_data.to_dict(orient='records'))

    @app.route('/api/events', methods=['GET'])
    def get_events():
        """API to fetch event data."""
        _, event_data, _ = load_data()
        if event_data is None:
            return jsonify({'error': 'Failed to load event data'}), 500
        event_data['Start_Date'] = event_data['Start_Date'].dt.strftime('%Y-%m-%d')
        return jsonify(event_data.to_dict(orient='records'))

    @app.route('/api/change_points', methods=['GET'])
    def get_change_points():
        """API to fetch change point results."""
        _, _, change_points = load_data()
        if change_points is None:
            return jsonify({'error': 'Failed to load change point data'}), 500
        change_points['Change_Point_Date'] = change_points['Change_Point_Date'].dt.strftime('%Y-%m-%d')
        return jsonify(change_points.to_dict(orient='records'))