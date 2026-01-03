WITH txs AS (
  SELECT `hash`, to_address, gas_price.bignumeric_value as gas_price
  FROM `bigquery-public-data.goog_blockchain_arbitrum_one_us.transactions`
  WHERE block_timestamp >= TIMESTAMP('2024-01-01') AND block_timestamp < TIMESTAMP('2026-01-01')
  AND to_address IS NOT NULL
),
receipts AS (
  SELECT transaction_hash, gas_used
  FROM `bigquery-public-data.goog_blockchain_arbitrum_one_us.receipts`
  WHERE block_timestamp >= TIMESTAMP('2024-01-01') AND block_timestamp < TIMESTAMP('2026-01-01')
)
SELECT
  t.to_address as contract_address,
  SUM(r.gas_used * t.gas_price) as total_gas_fees_wei,
  COUNT(*) as tx_count
FROM
  txs t
JOIN
  receipts r ON t.`hash` = r.transaction_hash
GROUP BY
  contract_address
ORDER BY
  total_gas_fees_wei DESC
LIMIT 10
