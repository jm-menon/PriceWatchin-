# PriceWatchin-
A full-stack price tracking platform that simulates multiple e-commerce vendors, continuously scrapes product prices, stores historical data, exposes analytics APIs, caches frequently accessed queries with Redis, and includes load testing and observability tooling.

## Summary
I have 5 simulator ecommerce sites: Vendor-1, Vendor-2, Vendor-3, Vendor-4, Vendor-5
each of these + the scrapper is will run from docker along with a tracker api which keeps in track of the price history ad does analysis of the price values across vendors.
Scrapper will perform a health check before scrapping a particular sight.

The tracker keeps track of:
add a history api end for each vendor
output the best price for a product-> or rather give result in a sorted manner


## Features
* Simulated ecosystem of **5 independent e-commerce websites**
* Automated scraper that periodically collects product prices
* PostgreSQL database storing complete historical price data
* FastAPI Tracker API for querying price history
* Redis caching with cache invalidation
* Dockerized microservice architecture
* Load testing using Locust
* Monitoring using Prometheus and Grafana
* Responsive frontend for interacting with tracker APIs
* Post-quantum secured channel between scraper and vendor sites (hybrid X25519 + ML-KEM-768)

---

## Tech Stack
### Backend
* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis

### Post-Quantum Cryptography
* liboqs / oqs-python
* ML-KEM-768 (key encapsulation)
* X25519 (classical hybrid component)
* ML-DSA (message signing)

### Infrastructure

* Docker
* Docker Compose

### Monitoring

* Prometheus
* Grafana

### Performance Testing

* Locust
* Pytest

### Frontend

* React

---

# Architecture
                ┌──────────────────────┐
                │     Frontend UI      │
                └──────────┬───────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Tracker API   │
                  │    (FastAPI)    │
                  └────────┬────────┘
                           │
                 Cache Hit │
                           ▼
                      ┌────────┐
                      │ Redis  │
                      └────────┘
                           │
                 Cache Miss │
                           ▼
                 ┌─────────────────┐
                 │   PostgreSQL    │
                 └────────┬────────┘
                          ▲
                          │
                 writes latest prices
                          │
                 ┌────────┴────────┐
                 │     Scraper     │
                 └────────┬────────┘
                          │
     ┌────────────┬────────┼────────┬────────────┐
     ▼            ▼        ▼        ▼            ▼
  Site 1       Site 2   Site 3   Site 4      Site 5
  
---

# PQC Security Layer

The channel between the **Scraper** and each **Vendor Site** simulator is secured with a hybrid post-quantum key exchange, implemented via `liboqs`/`oqs-python` and shared out of the `shared/` module so both the scraper and each vendor service can use the same primitives.

## Threat Model

Prices are fetched over HTTP between two services that, in a real deployment, would sit on different trust boundaries (scraper infra vs. third-party vendor). The PQC layer protects that link against:
* **Passive "harvest now, decrypt later" attacks** — a classical-only exchange (e.g. plain TLS with ECDHE) is at risk if traffic is recorded today and a sufficiently capable quantum computer breaks it later.
* **Payload tampering** — price data written to Postgres is only as trustworthy as the channel it arrived on, so responses are signed, not just encrypted.

## Key Exchange (Hybrid X25519 + ML-KEM-768)
Scraper (client) Vendor Site (server)
───────────────── ────────────────────

Generate X25519 keypair
Generate ML-KEM-768 keypair
│
│ ClientHello:
│ { x25519_pub, mlkem_pub }
├───────────────────────────────────────►
│ 3. Encapsulate against
│ mlkem_pub → (ct, ss_pq)
│ 4. Generate ephemeral
│ X25519 keypair, derive
│ ss_classical via ECDH
│
│ ServerHello:
│ { x25519_ephemeral_pub, mlkem_ct,
│ signature = ML-DSA_sign(transcript) }
◄───────────────────────────────────────┤
│
Decapsulate mlkem_ct → ss_pq
Derive ss_classical via ECDH
Verify ML-DSA signature over transcript
│
session_key = KDF(ss_classical || ss_pq)
─────────────────────────────────────────
Symmetric channel (AEAD) used for all
subsequent price-fetch requests/responses


**Why hybrid, not PQC-only:** combining X25519 with ML-KEM-768 means the channel stays secure as long as *either* the classical Diffie-Hellman assumption or the underlying lattice (Module-LWE) assumption holds — a standard hedge recommended during the PQC transition period, in case a weakness is later found in ML-KEM.

**Session key derivation:** the classical shared secret (`ss_classical`) and the post-quantum shared secret (`ss_pq`) are concatenated and passed through a KDF to produce the symmetric session key used to encrypt the actual price payloads.

## Signing Layer (ML-DSA)

Each vendor site signs its handshake transcript (and can additionally sign individual price responses) with **ML-DSA**, giving the scraper a way to authenticate *which* vendor it's actually talking to and detect tampering in transit — independent of whether the transport-layer encryption is later broken.

## Where it Sits in the Data Flow
Scraper ──[PQC handshake: X25519 + ML-KEM-768]──► Vendor Site
◄──[ML-DSA-signed, AEAD-encrypted price data]──┘
Scraper ──[plain internal write]──► PostgreSQL



The PQC layer only wraps the **scraper ↔ vendor** hop — internal traffic to Postgres/Redis/the Tracker API stays on the existing Docker-network trust boundary and isn't in scope for this layer.

## Benchmarking

Handshake and end-to-end request overhead introduced by the hybrid key exchange are measured the same way the rest of the platform is load-tested — via Locust, with latency and throughput surfaced through the existing Prometheus/Grafana stack rather than a separate tool.

---

# Data Flow

1. Five simulated e-commerce services expose product APIs.
2. The scraper periodically fetches product prices from every vendor over the PQC-secured channel described above.
3. Normalized price data is stored in PostgreSQL.
4. Whenever new prices are written:

   * Redis cache entries related to that product are invalidated.
5. The frontend queries the Tracker API.
6. Tracker API:

   * returns cached results from Redis if available,
   * otherwise queries PostgreSQL,
   * caches the response,
   * returns the data to the client.

---

# Monitoring

The project includes application monitoring using Prometheus and Grafana.

Metrics currently collected include:

* Total API requests
* Request latency
* Redis cache hits
* Redis cache misses
* Scraper request count
* Scraper latency

---

# Load Testing

Locust is used to simulate concurrent users against the Tracker API.

Example endpoints tested:

* `/tracker/price_history/{product_id}/{date_from}/{date_to}`
* `/tracker/cheapest_product/{product_id}/{date_from}/{date_to}`
* `/tracker/product_vendor_history/{product_id}/{vendor_id}/{date_from}/{date_to}`

---

# Project Structure
PriceWatchin/
│
├── frontend/
├── tracker_api/
├── workers/
│ └── scraper/
├── simulators/
│ ├── ecomm-site-1/
│ ├── ecomm-site-2/
│ ├── ecomm-site-3/
│ ├── ecomm-site-4/
│ └── ecomm-site-5/
├── monitoring/
│ ├── prometheus.yml
│ └── grafana/
├── scripts/
├── shared/
│ └── pqc/ # hybrid X25519 + ML-KEM-768 key exchange, ML-DSA signing
├── docker-compose.yml
└── README.md


---

# Running the Project

Clone the repository

```bash
git clone <repository-url>
cd PriceWatchin
```

Start all services

```bash
docker compose up --build
```

Available services

| Service     | Port       |
| ----------- | ---------- |
| Frontend    | 5173       |
| Tracker API | 8007       |
| PostgreSQL  | 5432       |
| Redis       | 6379       |
| Prometheus  | 9090       |
| Grafana     | 3000       |
| Site 1      | 8001       |
| Site 2      | 8002       |
| Site 3      | 8003       |
| Site 4      | 8004       |
| Site 5      | 8005       |

---

# Future Improvements

* Deploy the full platform to the cloud
* User authentication
* Email price alerts
* Price trend visualizations
* Product search
* Distributed scraping workers
* CI/CD pipeline
* Kubernetes deployment

---

# Screenshots

## Frontend
<img width="2664" height="1796" alt="image" src="https://github.com/user-attachments/assets/ce7dde31-cfe8-4582-9b97-2aa71b8eba8b" />
<img width="2596" height="1652" alt="image" src="https://github.com/user-attachments/assets/7141bb86-19e7-4e34-81e2-aec3f2722e8f" />
<img width="2776" height="1824" alt="image" src="https://github.com/user-attachments/assets/75f3c015-6f6d-4f9d-9a41-68a80feed35d" />
<img width="2668" height="1812" alt="image" src="https://github.com/user-attachments/assets/c2c2b75c-e3d5-4aac-8cdf-40a05124cfd8" />
<img width="2462" height="1676" alt="image" src="https://github.com/user-attachments/assets/b79e633b-ec90-40cf-b0b2-a206a3b9e73e" />



## Grafana Dashboard

<img width="2918" height="1840" alt="image" src="https://github.com/user-attachments/assets/4c5f845b-a571-4311-93bc-a7cbf06e5052" />
<img width="2916" height="1654" alt="image" src="https://github.com/user-attachments/assets/31a65c55-ee3c-4fbf-8aa0-1f7956f8267b" />


## Prometheus Metrics

<img width="882" height="638" alt="image" src="https://github.com/user-attachments/assets/00293cd0-e8c3-49d0-a244-dc9eac067017" />


## Locust Load Testing

<img width="1726" height="1740" alt="image" src="https://github.com/user-attachments/assets/30d06208-d160-4c13-b8cf-cb2904712f8d" />


---

# License

MIT License
