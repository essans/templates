import boto3
from botocore.exceptions import ClientError 
import base64
import os
from pathlib import Path
from tqdm import tqdm 
from types import SimpleNamespace
from typing import Any

def get_aws_secret(secret_name: str, region_name: str) -> Any:
    session = boto3.Session()
    client = session.client('secretsmanager', region_name=region_name or os.getenv('AWS_REGION'))
    try:
        resp = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
    if 'SecretString' in resp:
        return resp['SecretString']
    elif 'SecretBinary' in resp:
        try:
            return base64.b64decode(resp['SecretBinary']).decode('utf-8', errors='ignore')
        except Exception:
            return None
    return None


def set_ec2_credentials(secret_name: str, region: str) -> Any:
    
    try:
        secret_val = get_aws_secret(secret_name, region)

        if secret_val:
            os.environ['HF_TOKEN'] = secret_val.strip()
            print("HF_TOKEN set from AWS Secrets Manager.")
        else:
            print(f"Warning: could not fetch secret {secret_name} from AWS Secrets Manager.")
    except Exception as e:
      print(f"AWS Secrets Manager setup failed: {e}")


def s3_buckets() -> list[str]:
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])]



def s3_ls(bucket_name: str, prefix: str = "") -> list[str]:
    """
    List the contents (keys) of an S3 bucket.
    Args:
        bucket_name (str): Name of the S3 bucket.
        prefix (str): Optional prefix to filter objects.
    Returns:
        List[str]: List of object keys in the bucket.
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys



def s3_download_files(local_dest_folder: Path,
                      run_cfg: SimpleNamespace,
                      force: bool = False
                      ) -> None:
    """
    Download a list of files from an S3 bucket to a local folder.
    Args:
        bucket_name (str): Name of the S3 bucket.
        s3_paths (list[str]): List of S3 object keys to download.
        local_dest_folder (str): Local directory to save files.
        force (bool): If True, download even if file exists locally.
    """
    s3 = boto3.client("s3")
    os.makedirs(local_dest_folder, exist_ok=True)

    source_dir = run_cfg.datasets.dataset1.s3_path
    print(f'source_path: {source_dir}')

    bucket_name, prefix = bucket, path = str(source_dir).split('/', 1)

    s3_paths_list = s3_ls(bucket_name, prefix)
    print(s3_paths_list)
    
    for s3_path in tqdm(s3_paths_list, desc="Downloading S3 files"):
        local_path = os.path.join(local_dest_folder, os.path.basename(s3_path))
        if not force and os.path.exists(local_path):
            print(f"Skipping {local_path}, already exists.")
            continue
        try:
            s3.download_file(bucket_name, s3_path, local_path)
            print(f"Downloaded {s3_path} to {local_path}")
        except Exception as e:
            print(f"Failed to download {s3_path}: {e}")


def upload_directory_to_s3(local_dir: str, bucket_name: str, s3_prefix: str = "") -> None:
    """
    Upload all files from a local directory to a specified S3 bucket path.
    Args:
        local_dir (str): Path to the local directory to upload.
        bucket_name (str): Name of the S3 bucket.
        s3_prefix (str): S3 prefix (folder path in the bucket) to upload files to.
    """
    s3_client = boto3.client("s3")
    local_dir = os.path.abspath(local_dir)
    if not os.path.isdir(local_dir):
        raise ValueError(f"{local_dir} is not a valid directory.")
    # Walk through local_dir and upload each file
    files_to_upload = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            full_path = os.path.join(root, file)
            # S3 key: prefix + relative path from local_dir
            rel_path = os.path.relpath(full_path, local_dir)
            s3_key = os.path.join(s3_prefix, rel_path).replace("\\", "/")
            files_to_upload.append((full_path, s3_key))
    for full_path, s3_key in tqdm(files_to_upload, desc="Uploading to S3"):
        try:
            s3_client.upload_file(full_path, bucket_name, s3_key)
            print(f"Uploaded {full_path} to s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Failed to upload {full_path} to {s3_key}: {e}")


def upload_file_to_s3(local_file_path: str, bucket_name: str, s3_prefix: str = "") -> None:
    """
    Upload a single file to a specified S3 bucket and prefix, preserving the file name.
    Args:
        local_file_path (str): Path to the local file to upload.
        bucket_name (str): Name of the S3 bucket.
        s3_prefix (str): S3 prefix (folder path in the bucket) to upload the file to.
    """
    import boto3
    import os
    s3_client = boto3.client("s3")
    if not os.path.isfile(local_file_path):
        raise ValueError(f"{local_file_path} is not a valid file.")
    file_name = os.path.basename(local_file_path)
    s3_key = os.path.join(s3_prefix, file_name).replace("\\", "/") if s3_prefix else file_name
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
        print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {local_file_path} to {s3_key}: {e}")