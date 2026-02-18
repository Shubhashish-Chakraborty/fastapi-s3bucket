import os
from dotenv import load_dotenv
import boto3

s3 = boto3.client('s3')

def LOAD_ENV():
  load_dotenv()
  global BUCKET_NAME
  BUCKET_NAME = os.getenv("BUCKET_NAME")
  if not BUCKET_NAME:
    raise Exception("ENV VARIABLES NOT FOUND!")
  
def main():
  try:
    with open("fileurls.txt" , "w") as f:
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
          f.write(url + "\n")
          print(f"Generated: {key}")
          totalFiles += 1

  except Exception as e:
    print(f"What went wrong: {e}")

if __name__ == "__main__":
  LOAD_ENV()
  main()