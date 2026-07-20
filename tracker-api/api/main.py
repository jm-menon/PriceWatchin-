from fastapi import FastAPI
from routes import router as product_router
import uvicorn

app = FastAPI(title="Tracker API", 
              description="API for Tracker", 
              version="1.0.0")

app.include_router(product_router, prefix="/tracker")

@app.get("/health")
async def health_check():
    return {"status": "healthy!"}

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)