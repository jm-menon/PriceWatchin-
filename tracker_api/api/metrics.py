from prometheus_client import Counter, Histogram

REQUEST_COUNT= Counter(
    "tracker_requests_total",
    "Total API requests"
)

REQUEST_LATENCY= Histogram(
    "tracker_request_duration_seconds",
    "Request latency"
)
CACHE_HITS = Counter(
    "redis_cache_hits_total",
    "Number of cache hits"
)

CACHE_MISSES = Counter(
    "redis_cache_misses_total",
    "Number of cache misses"
)