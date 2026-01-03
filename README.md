# Layer-2 Ecosystem Analysis

This repository contains the source code and data collection scripts for our research on Ethereum Layer-2 scaling solutions, specifically analyzing the economic and performance characteristics of Arbitrum and Optimism before and after EIP-4844.

## Repository Structure

- `src/`: Core Python scripts for data collection (`collect_data.py`), economic modeling (`plot_economics.py`), and visualization (`visualize.py`).
- `src/queries/`: SQL queries used to extract metric data from Google BigQuery (public blockchain datasets).
- `requirements.txt`: Python package dependencies.

## Reproducibility

### Prerequisites
- Python 3.8+
- Google Cloud Credentials (for BigQuery access)

### Setup
```bash
pip install -r requirements.txt
```

### Usage
1. **Data Collection:**
   Extracts raw metrics from public BigQuery datasets.
   ```bash
   python3 src/collect_data.py
   ```

2. **Analysis & Visualization:**
   Generates the figures and statistical statistics presented in the paper.
   ```bash
   python3 src/plot_economics.py  # Generates Figure 5 (Economics) & Table 3 stats
   python3 src/visualize.py       # Generates all other performance plots
   ```

## Citation

BibTeX citation will be added upon acceptance.
