import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class S3Uploader:
    """Reusable utility for uploading project results to Amazon S3."""

    def __init__(self):
        self.bucket = os.getenv("AWS_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION_NAME")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not all([self.bucket, self.aws_access_key, self.aws_secret_access_key]):
            raise ValueError(
                "Missing AWS credentials. Set AWS_BUCKET_NAME, "
                "AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY in your environment."
            )

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region,
        )

    def upload(self, local_path: str, s3_key: str | None = None) -> bool:
        """
        Upload a file to the configured S3 bucket.
        If s3_key is not provided, a timestamped key under rankings/ is generated.
        """
        if s3_key is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            s3_key = f"rankings/{timestamp}_{os.path.basename(local_path)}"

        try:
            self.s3.upload_file(local_path, self.bucket, s3_key)
            print(f"[AWS] Uploaded {local_path} -> s3://{self.bucket}/{s3_key}")
            return True
        except Exception as e:
            print(f"[AWS ERROR] {e}")
            return False

    def list_files(self):
        """List all objects currently in the S3 bucket."""
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket)
            if "Contents" in response:
                print(f"\n--- Files in {self.bucket} ---")
                for obj in response["Contents"]:
                    print(f"{obj['Key']} ({obj['Size']} bytes)")
            else:
                print("The bucket is currently empty.")
        except Exception as e:
            print(f"Could not list files: {e}")