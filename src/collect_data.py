import os
from google.cloud import bigquery
import pandas as pd

def run_query(query_path, output_path):
    client = bigquery.Client(project='l2-mam')
    
    with open(query_path, 'r') as f:
        query = f.read()
        
    print(f"Executing query from {query_path}...")
    try:
        df = client.query(query).to_dataframe()
        df.to_csv(output_path, index=False)
        print(f"Saved results to {output_path} ({len(df)} rows)")
    except Exception as e:
        print(f"Error executing query {query_path}: {e}")

def main():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    queries = [
        # Run Daily Metrics
        ('src/queries/arbitrum_daily_metrics.sql', 'data/arbitrum_daily.csv'),
        ('src/queries/optimism_daily_metrics.sql', 'data/optimism_daily.csv'),
        ('src/queries/ethereum_daily_metrics.sql', 'data/ethereum_daily.csv'),
    
        # Run Event Studies
        ('src/queries/arbitrum_event_hourly.sql', 'data/arbitrum_event.csv'),
        ('src/queries/optimism_event_hourly.sql', 'data/optimism_event.csv'),

        # Run Workload Analysis (Top Contracts)
        ('src/queries/arbitrum_top_contracts.sql', 'data/arbitrum_top_contracts.csv'),
        ('src/queries/optimism_top_contracts.sql', 'data/optimism_top_contracts.csv')
    ]
    
    for query_path, output_path in queries:
        run_query(query_path, output_path)

if __name__ == "__main__":
    main()
