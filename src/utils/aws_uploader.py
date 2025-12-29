import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

"""
S3Uploader Module
-----------------
A reusable utility for uploading project results to Amazon S3.
Ported from MMA Simulation Project v1.2.
"""

load_dotenv()

class S3Uploader:
    def __init__(self):
        #load from .env
        load_dotenv()

        #aws credentials access

        self.bucket = os.getenv ("AWS_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION_NAME")

        self.aws_access_key= os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region
        )
        print("DEBUG:", self.aws_access_key, self.aws_secret_access_key)

    def upload(self, local_path, s3_key):
        """ Uploads a file to s3 bucket """
        
        #create timestamp key
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

        #inject timestamp into filename
        timestamped_key = f"rankings/{timestamp}_{os.path.basename(local_path)}"

        try:
            self.s3.upload_file(local_path, self.bucket, timestamped_key)
            print(f"[AWS] Uploaded {local_path} -> s3://{self.bucket}/{timestamped_key}")
            return True
        except Exception as e:
            print(f"[AWS ERROR] {e}")
            return False
        
    def list_files(self):
        """ Lists all files currently in the S3 bucket """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket)
        
            if 'Contents' in response:
                print(f"\n--- Files in {self.bucket} ---")
                for obj in response['Contents']:
                    print(f"{obj['Key']}  ({obj['Size']} bytes)")
            else:
                print("The bucket is currently empty.")
            
        except Exception as e:
            print(f"Could not list files: {e}")