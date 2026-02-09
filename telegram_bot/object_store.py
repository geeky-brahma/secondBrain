import boto3
import os
from dotenv import load_dotenv
load_dotenv()

ENDPOINT_URL = os.getenv("ENDPOINT_URL")
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")

def s3_client():
    s3 = boto3.client(
        service_name='s3',
        # Provide your R2 endpoint: https://<ACCOUNT_ID>.r2.cloudflarestorage.com
        endpoint_url=ENDPOINT_URL,
        # Provide your R2 Access Key ID and Secret Access Key
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name='auto',  # Required by boto3, not used by R2
    )
    return s3

# Upload a file
def upload_file(file_path: str, object_name: str):   
    s3 = s3_client()
    s3.upload_file(file_path, "second-brain", object_name)
    print(f'Uploaded {object_name} to bucket second-brain')

# Download a file
def download_file(object_name: str, file_path: str):
    s3 = s3_client()
    s3.download_file("second-brain", object_name, file_path)
    print(f'Downloaded {object_name} from bucket second-brain to {file_path}')

# List objects
def list_objects():
    s3 = s3_client()
    response = s3.list_objects_v2(Bucket="second-brain")
    for obj in response.get('Contents', []):
        print(f"Object: {obj['Key']}")

# upload_file('../image.jpeg', 'image.jpg')