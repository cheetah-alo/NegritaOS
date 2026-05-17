# EBM Explainability Report: EBM

## Artifact Summary
- Main effect plots: 10
- Interaction plots: 0
- Local explanation plots: 10
- Term curve rows: 1296
- Top rule candidates: 100
- Interaction rows: 0

## Top Global Terms
| term | score |
| --- | ---: |
| gateway_memory_utilization_avg_1h | 0.216424 |
| level_distinct_ipaddress_count_1h_was_missing | 0.105497 |
| gateway_cpu_avg_1h | 0.073831 |
| level_distinct_proxy_count_1h | 0.067772 |
| gateway_tx_op_band_avg_1h_was_missing | 0.054586 |
| gateway_cpu_avg_1h_was_missing | 0.050578 |
| gateway_client_associations_sum_1h | 0.050511 |
| extender_memory_utilization_avg_1h | 0.039940 |
| gateway_noise_band_avg_1h_was_missing | 0.035774 |
| level_rxlevel_avg_1h | 0.026184 |

## Top Main Effects
| feature | max_abs_score | mean_abs_score | nonzero_bins |
| --- | ---: | ---: | ---: |
| gateway_memory_utilization_avg_1h | 1.217508 | 0.460766 | 65 |
| gateway_temperature_avg_1h | 1.089316 | 0.057308 | 62 |
| level_rxlevel_range_1h | 1.009568 | 0.561817 | 122 |
| gateway_channel_automatic_change_24_sum_1h | 0.877228 | 0.400631 | 31 |
| gateway_band_steering_no_response_sum_1h | 0.746056 | 0.483555 | 11 |
| level_distinct_ipaddress_count_1h | 0.645873 | 0.322940 | 2 |
| level_distinct_ipaddress_count_1h_was_missing | 0.560168 | 0.309200 | 2 |
| extender_memory_utilization_avg_1h | 0.530380 | 0.103363 | 73 |
| gateway_cpu_avg_1h | 0.482099 | 0.281661 | 69 |
| gateway_tx_op_band_avg_1h | 0.381132 | 0.040691 | 125 |

## Top Interaction Pairs
No interaction rows available.

## Top Rule Candidates
| rank | feature | condition | abs_score_contribution | support_pct | direction |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | gateway_memory_utilization_avg_1h | gateway_memory_utilization_avg_1h in [7.069590559590667e-08, 7.09913764371074e-08) | 1.217508 | 0.00729135 | increases_churn |
| 2 | gateway_temperature_avg_1h | gateway_temperature_avg_1h in [0.0, 3.5) | 1.089316 | 0.00135392 | decreases_churn |
| 3 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.2289999999999992, 0.238999999999999) | 1.009568 | 0.00000206 | increases_churn |
| 4 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.2394999999999996, 0.25200000000000067) | 0.982327 | 0.00000325 | increases_churn |
| 5 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.21899999999999942, 0.2264999999999997) | 0.946490 | 0.00000222 | increases_churn |
| 6 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.2264999999999997, 0.2289999999999992) | 0.946490 | 0.00000222 | increases_churn |
| 7 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.17749999999999844, 0.1850000000000005) | 0.918384 | 0.00000277 | increases_churn |
| 8 | gateway_memory_utilization_avg_1h | gateway_memory_utilization_avg_1h in [9.369774435259821e-08, 1.0126751080972373e-07) | 0.900854 | 0.00037839 | increases_churn |
| 9 | gateway_channel_automatic_change_24_sum_1h | gateway_channel_automatic_change_24_sum_1h in [25.5, 26.5) | 0.877228 | 0.00001213 | increases_churn |
| 10 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.2134999999999998, 0.21899999999999942) | 0.837823 | 0.00000325 | increases_churn |
| 11 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.7544999999999984, 13.665000000000003) | 0.828704 | 0.00000222 | increases_churn |
| 12 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.5905000000000005, 0.7544999999999984) | 0.828265 | 0.00000214 | increases_churn |
| 13 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.5449999999999999, 0.5905000000000005) | 0.827950 | 0.00000206 | increases_churn |
| 14 | level_rxlevel_range_1h | level_rxlevel_range_1h in [0.4580000000000002, 0.4949999999999992) | 0.827705 | 0.00000206 | increases_churn |
| 15 | gateway_channel_automatic_change_24_sum_1h | gateway_channel_automatic_change_24_sum_1h in [31.5, 33.5) | 0.826898 | 0.00001086 | increases_churn |
