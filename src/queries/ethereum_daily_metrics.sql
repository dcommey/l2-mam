SELECT
  DATE(block_timestamp) AS metric_date,
  COUNT(*) AS tx_count,
  AVG(gas_price) as avg_gas_price,
  COUNT(DISTINCT from_address) as active_addresses,
  SAFE_DIVIDE(COUNTIF(receipt_status = 0), COUNT(*)) AS failure_rate
FROM
  `bigquery-public-data.crypto_ethereum.transactions`
WHERE
  block_timestamp >= TIMESTAMP('2024-01-01')
  AND block_timestamp < TIMESTAMP('2026-01-01')
GROUP BY
  metric_date
ORDER BY
  metric_date ASC
