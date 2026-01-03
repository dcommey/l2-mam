import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for IEEE papers
plt.style.use('seaborn-v0_8-paper')
sns.set_context("paper", font_scale=1.5)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.grid'] = True
plt.rcParams['figure.figsize'] = (10, 6)

def load_data():
    arb = pd.read_csv('data/arbitrum_daily.csv', parse_dates=['metric_date'])
    opt = pd.read_csv('data/optimism_daily.csv', parse_dates=['metric_date'])
    eth = pd.read_csv('data/ethereum_daily.csv', parse_dates=['metric_date'])
    
    arb_event = pd.read_csv('data/arbitrum_event.csv', parse_dates=['metric_hour'])
    opt_event = pd.read_csv('data/optimism_event.csv', parse_dates=['metric_hour'])
    
    return arb, opt, eth, arb_event, opt_event



def plot_gas_price(arb, opt, eth):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # L2 Gas (Left Axis)
    ax1.plot(arb['metric_date'], arb['avg_gas_price'] / 1e9, label='Arbitrum (Gwei)', color='blue', alpha=0.8)
    ax1.plot(opt['metric_date'], opt['avg_gas_price'] / 1e9, label='Optimism (Gwei)', color='red', alpha=0.8)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('L2 Gas Price (Gwei)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_yscale('log')
    
    # L1 Gas (Right Axis)
    ax2 = ax1.twinx()
    ax2.plot(eth['metric_date'], eth['avg_gas_price'] / 1e9, label='Ethereum L1 (Gwei)', color='grey', linestyle='--', alpha=0.5)
    ax2.set_ylabel('L1 Gas Price (Gwei)', color='grey')
    ax2.tick_params(axis='y', labelcolor='grey')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.title('Longitudinal Analysis of Gas Prices (2024)')
    plt.tight_layout()
    plt.savefig('paper/figures/gas_price_longitudinal.pdf')
    plt.close()

def plot_tps(arb, opt, eth):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Convert to TPS (Daily count / 86400)
    ax.plot(arb['metric_date'], arb['tx_count'] / 86400, label='Arbitrum', color='blue')
    ax.plot(opt['metric_date'], opt['tx_count'] / 86400, label='Optimism', color='red')
    ax.plot(eth['metric_date'], eth['tx_count'] / 86400, label='Ethereum', color='grey', linestyle='--')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Transactions Per Second (TPS)')
    ax.set_title('Daily Average Throughput (TPS)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('paper/figures/tps_comparison.pdf')
    plt.close()

def plot_event_study(arb_event, opt_event):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(arb_event['metric_hour'], arb_event['avg_gas_price'] / 1e9, label='Arbitrum', color='blue', marker='o')
    ax.plot(opt_event['metric_hour'], opt_event['avg_gas_price'] / 1e9, label='Optimism', color='red', marker='x')
    
    ax.set_xlabel('Hour (UTC)')
    ax.set_ylabel('Gas Price (Gwei)')
    ax.set_title('Event Study: Gas Dynamics during High Traffic (June 20, 2024)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('paper/figures/event_study_gas.pdf')
    plt.close()

def plot_cdf(arb, opt):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Calculate CDF
    sns.ecdfplot(data=arb, x='avg_gas_price', label='Arbitrum', color='blue')
    sns.ecdfplot(data=opt, x='avg_gas_price', label='Optimism', color='red')
    
    ax.set_xscale('log')
    ax.set_xlabel('Gas Price (Wei)')
    ax.set_ylabel('Cumulative Probability')
    ax.set_title('CDF of Transaction Gas Prices (2024-2025)')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('paper/figures/gas_cdf.pdf')
    plt.close()

def plot_daa(arb, opt, eth):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.lineplot(data=arb, x='metric_date', y='active_addresses', label='Arbitrum', color='blue')
    sns.lineplot(data=opt, x='metric_date', y='active_addresses', label='Optimism', color='red')
    sns.lineplot(data=eth, x='metric_date', y='active_addresses', label='Ethereum', color='gray', alpha=0.5)
    
    ax.set_yscale('log')
    ax.set_ylabel('Daily Active Addresses (Log Scale)')
    ax.set_xlabel('Date')
    ax.set_title('Network Adoption: Daily Active Addresses (2024-2025)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('paper/figures/daa_longitudinal.pdf')
    plt.close()

def calculate_correlations(arb, opt, eth):
    # Align data on date
    df = pd.merge(arb[['metric_date', 'avg_gas_price']], eth[['metric_date', 'avg_gas_price']], on='metric_date', suffixes=('_arb', '_eth'))
    df = pd.merge(df, opt[['metric_date', 'avg_gas_price']], on='metric_date')
    df.rename(columns={'avg_gas_price': 'avg_gas_price_opt'}, inplace=True)
    
    # Pearson Correlation
    corr_arb_eth = df['avg_gas_price_arb'].corr(df['avg_gas_price_eth'])
    corr_opt_eth = df['avg_gas_price_opt'].corr(df['avg_gas_price_eth'])
    
    print(f"Correlation (Arbitrum vs Ethereum): {corr_arb_eth:.4f}")
    print(f"Correlation (Optimism vs Ethereum): {corr_opt_eth:.4f}")
    
    return corr_arb_eth, corr_opt_eth

def main():
    os.makedirs('paper/figures', exist_ok=True)
    
    try:
        arb, opt, eth, arb_event, opt_event = load_data()
        
        plot_gas_price(arb, opt, eth)
        print("Generated gas_price_longitudinal.pdf")
        
        plot_tps(arb, opt, eth)
        print("Generated tps_comparison.pdf")
        
        plot_event_study(arb_event, opt_event)
        print("Generated event_study_gas.pdf")
        
        plot_cdf(arb, opt)
        print("Generated gas_cdf.pdf")

        plot_daa(arb, opt, eth)
        print("Generated daa_longitudinal.pdf")


        
        calculate_correlations(arb, opt, eth)
        
    except FileNotFoundError as e:
        print(f"Error loading data: {e}. Run collect_data.py first.")

if __name__ == "__main__":
    main()
