from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.get_data_from_s3 import get_s3_urls
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
  return {"message": "Python Backend is UP!!"}

@app.get("/data")
async def fetch_data():
  urls = get_s3_urls()
  if (not urls):
    return {
      "message": "S3 Bucket is Empty!"
    }
  else:
    return {
      "files": urls,
      "count": len(urls)
    }