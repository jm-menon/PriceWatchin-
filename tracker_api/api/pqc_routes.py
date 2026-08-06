from fastapi import APIRouter
import time
from metrics import (
    CLASSICAL_HANDSHAKE_DURATION,
    PQC_HANDSHAKE_DURATION,
    HANDSHAKE_PAYLOAD_BYTES
)


router = APIRouter()

@router.get("/classical-handshake")
async def classical_handshake():

    start = time.perf_counter()

    time.sleep(0.003)

    latency = time.perf_counter() - start

    CLASSICAL_HANDSHAKE_DURATION.observe(latency)

    HANDSHAKE_PAYLOAD_BYTES.labels(
        type="classical"
    ).inc(32)

    return {
        "algorithm": "ECDH",
        "payload_bytes": 32,
        "latency_seconds": latency,
        "status": "success"
    }


@router.get("/hybrid-handshake")
async def hybrid_handshake():

    start = time.perf_counter()

    time.sleep(0.006)

    latency = time.perf_counter() - start

    PQC_HANDSHAKE_DURATION.observe(latency)

    HANDSHAKE_PAYLOAD_BYTES.labels(
        type="hybrid"
    ).inc(2272)

    return {
        "algorithm": "ECDH + ML-KEM",
        "payload_bytes": 2272,
        "latency_seconds": latency,
        "status": "success"
    }