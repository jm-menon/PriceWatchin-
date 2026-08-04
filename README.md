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

---

## Tech Stack
### Backend
* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis

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

```
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
```

---

# Data Flow

1. Five simulated e-commerce services expose product APIs.
2. The scraper periodically fetches product prices from every vendor.
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

```
PriceWatchin/
│
├── frontend/
├── tracker_api/
├── workers/
│   └── scraper/
├── simulators/
│   ├── ecomm-site-1/
│   ├── ecomm-site-2/
│   ├── ecomm-site-3/
│   ├── ecomm-site-4/
│   └── ecomm-site-5/
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
├── scripts/
├── shared/
├── docker-compose.yml
└── README.md
```

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


## Deploying to Render

This repository includes `render.yaml` for a Blueprint deployment. It creates the
public frontend, private tracker and vendor APIs, scraper worker, Render Postgres,
and Render Key Value. The tracker performs a one-time database schema and seed
initialization during its first deployment.

Private services and background workers require paid Render plans. Review the
Blueprint's selected plans before confirming deployment.

## Frontend production build

The frontend's production image is served by Nginx, not the Vite development
server. Build and run it locally with `docker compose up --build frontend`, then
open `http://localhost:5173`. The container exposes `/health` for deployment
health checks.
