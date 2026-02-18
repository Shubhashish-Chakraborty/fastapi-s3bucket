import os
from dotenv import load_dotenv
import boto3
from config import BUCKET_NAME

s3 = boto3.client('s3')
  
def get_s3_urls():
  URLS = []
  try:
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET_NAME) # handles large buckets automatically
    totalFiles = 0
    for page in pages:
        if "Contents" not in page:
            continue

    for obj in page["Contents"]:
        key = obj["Key"]
        url = s3.generate_presigned_url( # generate a temporary download link (valid 1 day)
            ClientMethod="get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": key
            },
            ExpiresIn=86400 # 1Day!
        )
        URLS.append(url)
        print(f"Generated: {key}")
        totalFiles += 1
    return URLS
  
  except Exception as e:
    print(f"What went wrong: {e}")

if __name__ == "__main__":
  LOAD_ENV()
  get_s3_urls()