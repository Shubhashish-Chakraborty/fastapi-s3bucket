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
  
def saveUrlToLocal(file_url):
  try:
    with open("./fileurls.txt" , "a") as f:
      f.write(file_url + "\n")
    print(f"FileUrl Stored in ./fileurls.txt: {file_url}")
  except Exception as e:
    print(f"Something went wrong in storing file locally: {e}")

def uploadFile(file_path, s3_file_name):
  try:
    s3.upload_file(
      file_path,
      BUCKET_NAME,
      s3_file_name,
    )
  
    fileUrl = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_file_name}"
    print("Uploaded Successfully")
    saveUrlToLocal(fileUrl)
  except Exception as e:
    print(f"What went Wrong: {e}")

def main():
  os.system("clear")
  # /Users/shubhashishchakraborty/Downloads/myLogo.png
  
  filePath_toupload = input("Enter the File Path to upload to s3: ")
  s3FileName = input("Enter the Name of S3 File: ")

  if (s3FileName.endswith(("png", "jpg", "jpeg", "pdf"))): # etcetc..
    uploadFile(file_path=filePath_toupload, s3_file_name=s3FileName)
  else:
    print("Upload failed: S3 File Name not with proper extension")

if __name__ == "__main__":
  LOAD_ENV()
  main()
