import numpy as np
import pandas as pd
import yaml
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'risk_categories.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def generate_securities(num_securities=500):
    """Generate synthetic securities master data."""
    np.random.seed(42)
    asset_classes = ['Equity', 'Fixed Income', 'Alternatives', 'Cash']
    
    # We create a dataframe with 500 securities distributed across asset classes
    df = pd.DataFrame({
        'ticker': [f'SEC_{i:04d}' for i in range(num_securities)],
        'asset_class': np.random.choice(asset_classes, num_securities, p=[0.5, 0.3, 0.1, 0.1]),
        'current_price': np.random.uniform(10, 1000, num_securities),
        'volatility': np.random.uniform(0.05, 0.3, num_securities),
        'adv_30d': np.random.uniform(10000, 1000000, num_securities),
        'bid_ask_spread_pct': np.random.uniform(0.0001, 0.0050, num_securities)
    })
    
    # Force lower ADV and higher spreads for Alternatives and some mid/small caps
    mid_small_mask = (df['asset_class'] == 'Alternatives') | (np.random.rand(num_securities) < 0.2)
    df.loc[mid_small_mask, 'adv_30d'] *= 0.1
    df.loc[mid_small_mask, 'bid_ask_spread_pct'] *= 3.0
    
    return df

def generate_portfolios(config):
    """Generate 50,000 synthetic portfolios based on risk categories."""
    np.random.seed(42)
    risk_cats = config.get('risk_categories', {})
    
    portfolios = []
    
    for category, details in risk_cats.items():
        num_ports = details['num_portfolios']
        for i in range(num_ports):
            portfolios.append({
                'portfolio_id': f'PORT_{category[:3]}_{i:06d}',
                'client_id': f'CLI_{category[:3]}_{i:06d}',
                'risk_category': category,
                'total_value': np.random.uniform(100000, 5000000),
                # We add slight random drift to the target allocations
                'equity_weight': max(0, details['target_allocations']['Equity'] + np.random.normal(0, 0.05)),
                'fixed_income_weight': max(0, details['target_allocations']['Fixed Income'] + np.random.normal(0, 0.03)),
                'alternatives_weight': max(0, details['target_allocations']['Alternatives'] + np.random.normal(0, 0.02)),
                'cash_weight': max(0, details['target_allocations']['Cash'] + np.random.normal(0, 0.01))
            })
            
    df = pd.DataFrame(portfolios)
    # Normalize weights so they sum to 1
    weight_cols = ['equity_weight', 'fixed_income_weight', 'alternatives_weight', 'cash_weight']
    df[weight_cols] = df[weight_cols].div(df[weight_cols].sum(axis=1), axis=0)
    
    return df

def generate_market_returns(num_securities=500, num_days=252):
    """Generate correlated market returns using a multivariate normal distribution."""
    np.random.seed(42)
    
    # 1. Expected Return Vector (Daily)
    # Assuming annualized returns between 2% and 15%, divide by 252 for daily
    annual_returns = np.random.uniform(0.02, 0.15, num_securities)
    mu = annual_returns / 252.0
    
    # 2. Covariance Matrix
    # Using a 3-factor model to ensure a valid, realistic covariance matrix
    num_factors = 3
    factor_exposures = np.random.uniform(0.5, 1.5, (num_securities, num_factors))
    # Factor covariance (assume independent factors for simplicity, approx 15% annualized volatility)
    factor_cov = np.eye(num_factors) * (0.15 / np.sqrt(252))**2  
    
    # Idiosyncratic variance (specific risk to each security, 10-30% annualized)
    idiosyncratic_var = np.diag(np.random.uniform(0.10, 0.30, num_securities)**2 / 252.0)
    
    # Total covariance matrix: B * F * B.T + Delta
    cov_matrix = factor_exposures @ factor_cov @ factor_exposures.T + idiosyncratic_var
    
    # 3. Sample Returns
    returns = np.random.multivariate_normal(mu, cov_matrix, num_days)
    
    # Create DataFrame
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=num_days, freq='B')
    returns_df = pd.DataFrame(returns, index=dates, columns=[f'SEC_{i:04d}' for i in range(num_securities)])
    
    return returns_df, cov_matrix

def generate_tax_lots(portfolios_df, securities_df):
    """Generate detailed tax lots for each portfolio's positions."""
    np.random.seed(42)
    num_ports = len(portfolios_df)
    positions_per_port = 10
    total_positions = num_ports * positions_per_port
    
    port_ids = np.repeat(portfolios_df['portfolio_id'].values, positions_per_port)
    tickers = np.random.choice(securities_df['ticker'].values, total_positions)
    
    # Create 1 to 5 lots per position
    lots_per_pos = np.random.randint(1, 6, total_positions)
    total_lots = lots_per_pos.sum()
    
    lot_port_ids = np.repeat(port_ids, lots_per_pos)
    lot_tickers = np.repeat(tickers, lots_per_pos)
    
    # Random acquisition dates between 30 and 730 days ago
    days_ago = np.random.randint(30, 731, total_lots)
    today = pd.Timestamp.today().normalize()
    acq_dates = today - pd.to_timedelta(days_ago, unit='D')
    
    # Get current prices for cost basis calculation
    price_map = securities_df.set_index('ticker')['current_price'].to_dict()
    current_prices = np.array([price_map[t] for t in lot_tickers])
    
    # Randomize cost bases around +/- 20% of current market price
    cost_bases = current_prices * np.random.uniform(0.8, 1.2, total_lots)
    
    # Randomize shares between 10 and 1000
    shares = np.random.uniform(10, 1000, total_lots)
    
    tax_lots_df = pd.DataFrame({
        'portfolio_id': lot_port_ids,
        'security_ticker': lot_tickers,
        'shares': shares,
        'cost_basis': cost_bases,
        'acquisition_date': acq_dates
    })
    return tax_lots_df

if __name__ == "__main__":
    print("Loading config...")
    config = load_config()
    
    print("Generating securities...")
    securities_df = generate_securities()
    print(f"Generated {len(securities_df)} securities.")
    
    print("Generating portfolios...")
    portfolios_df = generate_portfolios(config)
    print(f"Generated {len(portfolios_df)} portfolios.")
    
    print("Generating market returns...")
    returns_df, cov_matrix = generate_market_returns()
    print(f"Generated {len(returns_df)} days of returns for {returns_df.shape[1]} securities.")
    print("Generating tax lots...")
    tax_lots_df = generate_tax_lots(portfolios_df, securities_df)
    print(f"Generated {len(tax_lots_df)} tax lots.")
    
    # Save to disk
    out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    os.makedirs(out_dir, exist_ok=True)
    
    securities_df.to_parquet(os.path.join(out_dir, 'securities.parquet'))
    portfolios_df.to_parquet(os.path.join(out_dir, 'portfolios.parquet'))
    returns_df.to_parquet(os.path.join(out_dir, 'market_returns.parquet'))
    tax_lots_df.to_parquet(os.path.join(out_dir, 'tax_lots.parquet'))
    np.save(os.path.join(out_dir, 'covariance_matrix.npy'), cov_matrix)
    print("Data generation complete. Saved to data/ directory.")
