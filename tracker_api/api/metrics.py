from prometheus_client import Counter, Histogram

REQUEST_COUNT= Counter(
    "tracker_requests_total",
    "Total API requests"
)

REQUEST_LATENCY= Histogram(
    "tracker_request_duration_seconds",
    "Request latency"
)
#this creates fyi:
#tracker_request_duration_seconds_bucket
#tracker_request_duration_seconds_count
#tracker_request_duration_seconds_sum


CACHE_HITS = Counter(
    "redis_cache_hits_total",
    "Number of cache hits"
)

CACHE_MISSES = Counter(
    "redis_cache_misses_total",
    "Number of cache misses"
)

CLASSICAL_HANDSHAKE_DURATION = Histogram(
    "classical_handshake_duration_seconds",
    "Latency of classical handshake"
)

PQC_HANDSHAKE_DURATION = Histogram(
    "pqc_handshake_duration_seconds",
    "Latency of hybrid PQC handshake"
)

HANDSHAKE_PAYLOAD_BYTES = Counter(
    "handshake_payload_bytes_total",
    "Total bytes exchanged during handshake",
    ["type"]
)
