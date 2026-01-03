WITH tx_metrics AS (
  SELECT
    TIMESTAMP_TRUNC(block_timestamp, HOUR) as metric_hour,
    COUNT(*) as total_txs,
    AVG(gas_price.bignumeric_value) as avg_gas
  FROM
    `bigquery-public-data.goog_blockchain_optimism_mainnet_us.transactions`
  WHERE
    DATE(block_timestamp) = '2024-06-20'
  GROUP BY
    metric_hour
),
receipt_metrics AS (
  SELECT
    TIMESTAMP_TRUNC(block_timestamp, HOUR) as metric_hour,
    COUNTIF(status = 0) as failed_txs
  FROM
    `bigquery-public-data.goog_blockchain_optimism_mainnet_us.receipts`
  WHERE
    DATE(block_timestamp) = '2024-06-20'
  GROUP BY
    metric_hour
)
SELECT
  t.metric_hour,
  t.total_txs as tx_count,
  t.avg_gas as avg_gas_price,
  SAFE_DIVIDE(r.failed_txs, t.total_txs) as failure_rate
FROM
  tx_metrics t
LEFT JOIN
  receipt_metrics r
ON
  t.metric_hour = r.metric_hour
ORDER BY
  metric_hour ASC
