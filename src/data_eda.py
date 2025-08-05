import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset
def load_data(file_path: str) -> pd.DataFrame:
    """Load Brent oil price data from CSV."""
    return pd.read_csv(file_path)

# 2. View initial rows
def preview_data(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Preview first n rows of the DataFrame."""
    return df.head(n)

# 3. Show DataFrame info
def show_info(df: pd.DataFrame):
    """Print DataFrame structure and data types."""
    df.info()

# 4. Show DataFrame shape
def show_shape(df: pd.DataFrame):
    """Print shape (rows, columns) of DataFrame."""
    print(f"Shape of dataset: {df.shape}")

# 5. Summary statistics
def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return summary statistics of numerical columns."""
    return df.describe()

# 6. Check for missing values
def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """Return count of missing values per column."""
    return df.isnull().sum()

# 7. Check for duplicates
def check_duplicates(df: pd.DataFrame) -> int:
    """Return count of duplicated rows."""
    return df.duplicated().sum()


# 8. Plot the time series data
def plot_brent_prices(df: pd.DataFrame, date_col: str = 'Date', price_col: str = 'Price'):
    """
    Plot Brent Oil prices over time, with properly formatted datetime x-axis.
    """
    # Ensure date column is datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Sort by date in case it's not sorted
    df = df.sort_values(by=date_col)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df[date_col], df[price_col], label='Brent Oil Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Brent Oil Prices Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

