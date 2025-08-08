import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Step 1: Data Preparation and EDA

def load_and_prepare_data():
    """
    Load Brent oil price data from CSV and event data, compute log returns.
    """
    # Load sample data from CSV
    price_data = pd.read_csv('F:/Change-point-analysis-and-statistical-modelling-of-time-series-data/data/BrentOilPrices.csv')
    price_data['Date'] = pd.to_datetime(price_data['Date'], format='mixed', dayfirst=False)
    price_data = price_data.rename(columns={'Price': 'Brent_Price'})
    price_data.set_index('Date', inplace=True)

    # Compute log returns
    price_data['Log_Returns'] = np.log(price_data['Brent_Price']).diff()

    # Load event data from Task 1
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
        ],
        'Source': [
            'https://www.eia.gov/todayinenergy/detail.php?id=51638',
            'https://www.reuters.com/article/us-iran-nuclear-oil/iran-oil-exports-dwindle-as-u.s.-sanctions-bite-idUSKCN1VJ0D1',
            'https://www.opec.org/opec_web/en/press_room/5945.htm',
            'https://www.cnbc.com/2023/10/09/oil-prices-jump-as-middle-east-violence-rattles-markets.html',
            'https://www.bloomberg.com/news/articles/2023/07/07/russia-faces-new-sanctions-on-oil-exports-as-west-tightens-grip',
            'https://www.reuters.com/business/energy/red-sea-attacks-disrupt-global-oil-shipping-routes-2023-12-18/',
            'https://www.spglobal.com/commodityinsights/en/market-insights/latest-news/oil/060125-opec-to-increase-production-in-2025',
            'https://www.bloomberg.com/news/articles/2025-04-01/us-china-trade-tensions-impact-oil-prices',
            'https://www.ft.com/content/iran-israel-tensions-2025-oil-price-spike',
            'https://www.bbc.com/news/business-51813878',
            'https://www.eia.gov/todayinenergy/detail.php?id=4265',
            'https://www.energy.gov/articles/doe-announces-spr-replenishment-purchases-2023'
        ]
    })
    event_data['Start_Date'] = pd.to_datetime(event_data['Start_Date'])

    return price_data, event_data

def exploratory_analysis(price_data, event_data):
    """
    Perform EDA: Plot raw price series and log returns, mark events.
    """
    # Plot raw price series
    plt.figure(figsize=(12, 6))
    plt.plot(price_data.index, price_data['Brent_Price'], label='Brent Oil Price')
    for event_date in event_data['Start_Date']:
        plt.axvline(x=event_date, color='r', linestyle='--', alpha=0.5, label='Events' if event_date == event_data['Start_Date'].iloc[0] else '')
    plt.title('Brent Oil Prices with Major Events')
    plt.xlabel('Date')
    plt.ylabel('Price (USD/bbl)')
    plt.legend()
    plt.savefig('brent_price_events.png')
    plt.show()

    # Plot log returns
    plt.figure(figsize=(12, 6))
    plt.plot(price_data.index, price_data['Log_Returns'], label='Log Returns')
    for event_date in event_data['Start_Date']:
        plt.axvline(x=event_date, color='r', linestyle='--', alpha=0.5, label='Events' if event_date == event_data['Start_Date'].iloc[0] else '')
    plt.title('Brent Oil Log Returns with Major Events')
    plt.xlabel('Date')
    plt.ylabel('Log Returns')
    plt.legend()
    plt.savefig('brent_log_returns.png')
    plt.show()

# Step 2: Bayesian Change Point Model
def bayesian_change_point_model(price_data):
    """
    Implement Bayesian Change Point model using PyMC.
    """
    # Prepare data
    prices = price_data['Brent_Price'].values
    n_points = len(prices)
    idx = np.arange(n_points)

    with pm.Model() as model:
        # Define switch point (tau) as discrete uniform prior
        tau = pm.DiscreteUniform('tau', lower=0, upper=n_points-1)

        # Define before and after means
        mu_1 = pm.Normal('mu_1', mu=18, sigma=5)  # Changed sd to sigma
        mu_2 = pm.Normal('mu_2', mu=18, sigma=5)  # Changed sd to sigma

        # Define switch function for mean
        mu = pm.math.switch(tau >= idx, mu_1, mu_2)

        # Define likelihood
        sigma = pm.HalfNormal('sigma', sigma=5) # Changed sd to sigma
        likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=prices) # Changed sd to sigma

        # Run MCMC sampler (reduced samples due to small dataset)
        trace = pm.sample(1000, tune=500, return_inferencedata=True, random_seed=42)

    return trace, idx

# Step 3: Interpret Model Output
def interpret_model(trace, price_data, event_data):
    """
    Analyze posterior distributions, identify change points, and associate with events.
    """
    # Check convergence
    summary = az.summary(trace, var_names=['tau', 'mu_1', 'mu_2', 'sigma'])
    print("Model Summary:")
    print(summary)

    # Plot trace for convergence diagnostics
    az.plot_trace(trace, var_names=['tau', 'mu_1', 'mu_2'])
    plt.savefig('trace_plots.png')
    plt.show()

    # Extract change point (tau) posterior
    tau_samples = trace.posterior['tau'].values.flatten()
    tau_mode = int(np.bincount(tau_samples).argmax())  # Most probable tau
    change_point_date = price_data.index[tau_mode]

    # Plot posterior of tau
    plt.figure(figsize=(12, 6))
    sns.histplot(tau_samples, bins=10, kde=True)  # Fewer bins due to small dataset
    plt.axvline(tau_mode, color='r', linestyle='--', label=f'Most Probable Change Point: {change_point_date.date()}')
    plt.title('Posterior Distribution of Change Point (tau)')
    plt.xlabel('Time Index')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig('tau_posterior.png')
    plt.show()

    # Quantify impact
    mu_1_samples = trace.posterior['mu_1'].values.flatten()
    mu_2_samples = trace.posterior['mu_2'].values.flatten()
    mu_1_mean = mu_1_samples.mean()
    mu_2_mean = mu_2_samples.mean()
    price_change = ((mu_2_mean - mu_1_mean) / mu_1_mean) * 100 if mu_1_mean != 0 else 0

    # Associate with events
    event_window = pd.Timedelta(days=7)  # 1-week window due to short sample
    associated_events = event_data[
        (event_data['Start_Date'] >= change_point_date - event_window) &
        (event_data['Start_Date'] <= change_point_date + event_window)
    ]

    # Generate insights
    insights = []
    if not associated_events.empty:
        for _, event in associated_events.iterrows():
            insight = (
                f"Following the {event['Event_Name']} ({event['Event_Type']}) around {event['Start_Date'].date()}, "
                f"the model detects a change point on {change_point_date.date()}, "
                f"with the average daily price shifting from ${mu_1_mean:.2f} to ${mu_2_mean:.2f}, "
                f"an {'increase' if mu_2_mean > mu_1_mean else 'decrease'} of {abs(price_change):.2f}%."
            )
            insights.append(insight)
    else:
        insights.append(
            f"Change point detected on {change_point_date.date()}, but no events found within 1-week window. "
            f"Average price shifted from ${mu_1_mean:.2f} to ${mu_2_mean:.2f}, "
            f"an {'increase' if mu_2_mean > mu_1_mean else 'decrease'} of {abs(price_change):.2f}%."
        )

    return change_point_date, insights, mu_1_mean, mu_2_mean, price_change, associated_events

if __name__ == '__main__':
    pass      