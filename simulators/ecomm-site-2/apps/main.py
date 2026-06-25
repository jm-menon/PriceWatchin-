from fastapi import FastAPI
from .routes import router as product_router
import uvicorn

app = FastAPI(title="E-commerce Site1 API", 
              description="API for E-commerce Site1", 
              version="1.0.0")

app.include_router(product_router, prefix="/products-site-2")

@app.get("/health")
async def health_check():
    return {"status": "healthy!"}

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
    print("E-commerce Site2 API is running on port", 8002)