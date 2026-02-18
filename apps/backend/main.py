from fastapi import FastAPI
from services.get_data_from_s3 import get_s3_urls
app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Python Backend is UP!!"}

@app.get("/data")
async def fetch_data():
  urls = get_s3_urls()
  return {
    "files": urls,
    "count": len(urls)
  }