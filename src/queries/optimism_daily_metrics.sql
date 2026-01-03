WITH tx_metrics AS (
  SELECT
    DATE(block_timestamp) as metric_date,
    COUNT(*) as total_txs,
    AVG(gas_price.bignumeric_value) as avg_gas_price,
    COUNT(DISTINCT from_address) as active_addresses
  FROM
    `bigquery-public-data.goog_blockchain_optimism_mainnet_us.transactions`
  WHERE
    block_timestamp >= TIMESTAMP('2024-01-01')
    AND block_timestamp < TIMESTAMP('2026-01-01')
  GROUP BY
    metric_date
),
receipt_metrics AS (
  SELECT
    DATE(block_timestamp) as metric_date,
    COUNTIF(status = 0) as failed_txs
  FROM
    `bigquery-public-data.goog_blockchain_optimism_mainnet_us.receipts`
  WHERE
    block_timestamp >= TIMESTAMP('2024-01-01')
    AND block_timestamp < TIMESTAMP('2026-01-01')
  GROUP BY
    metric_date
)
SELECT
  t.metric_date,
  t.total_txs as tx_count,
  t.avg_gas_price,
  t.active_addresses,
  SAFE_DIVIDE(r.failed_txs, t.total_txs) as failure_rate
FROM
  tx_metrics t
LEFT JOIN
  receipt_metrics r
ON
  t.metric_date = r.metric_date
ORDER BY
  metric_date ASC
