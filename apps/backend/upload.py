import os
import mimetypes
from dotenv import load_dotenv
from config import BUCKET_NAME
import boto3

s3 = boto3.client('s3')
  
def saveUrlToLocal(file_url):
  try:
    with open("./fileurls.txt" , "a") as f:
      f.write(file_url + "\n")
    print(f"FileUrl Stored in ./fileurls.txt: {file_url}")
  except Exception as e:
    print(f"Something went wrong in storing file locally: {e}")

def generate_view_url(key):
  """
  Create a temporary URL (1 day) that OPENS in browser
  """
  try:
    url = s3.generate_presigned_url(
      "get_object",
      Params={
        "Bucket": BUCKET_NAME,
        "Key": key,
        "ResponseContentDisposition": "inline"  # VIEW not download
      },
      ExpiresIn=86400  # 1 day
    )
    return url
  except Exception as e:
    print(f"Error generating presigned URL: {e}")
    return None


def uploadFile_previewable(file_path, s3_file_name): # this will store files and it will be a previewable file

    # check file exists
    if not os.path.isfile(file_path):
        print("File path invalid ❌")
        return

    try:
        # detect MIME type
        content_type, _ = mimetypes.guess_type(file_path)

        if content_type is None:
            content_type = "application/octet-stream"

        print(f"Detected Content-Type: {content_type}")

        # upload with metadata
        s3.upload_file(
            file_path,
            BUCKET_NAME,
            s3_file_name,
            ExtraArgs={
                "ContentType": content_type
            }
        )

        print("Uploaded Successfully ✅")

        # generate viewable link
        view_url = generate_view_url(s3_file_name)

        if view_url:
            print("\nView URL (valid 1 day):\n")
            print(view_url)
            saveUrlToLocal(view_url)

    except Exception as e:
        print(f"What went wrong: {e}")

  
def uploadFile(file_path, s3_file_name): # this will store the files, and it will be downloadable!
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
  # /Users/shubhashishchakraborty/Downloads/myLogo.png
  
  filePath_toupload = input("Enter the File Path to upload to s3: ")
  s3FileName = input("Enter the Name of S3 File: ")

  if (s3FileName.endswith(("png", "jpg", "jpeg", "pdf", "mp4"))): # etcetc..
    uploadFile_previewable(file_path=filePath_toupload, s3_file_name=s3FileName)
  else:
    print("Upload failed: S3 File Name not with proper extension")

if __name__ == "__main__":
  main()