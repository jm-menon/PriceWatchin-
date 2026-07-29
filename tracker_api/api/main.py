from fastapi import FastAPI
from routes import router as product_router
from prometheus_client import make_asgi_app
import uvicorn

app = FastAPI(
    title="Tracker API",
    description="API for Tracker",
    version="1.0.0"
)

app.include_router(product_router, prefix="/tracker")

@app.get("/health")
async def health_check():
    return {"status": "healthy!"}

# Mount Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)