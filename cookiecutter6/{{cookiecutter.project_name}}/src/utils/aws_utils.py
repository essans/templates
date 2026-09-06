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


def s3_ls2(bucket_name: str, prefix: str = "", folders_only: bool = False) -> list[str]:
    """List S3 objects or virtual folders beneath an optional prefix."""
    import boto3

    s3 = boto3.client("s3")

    request = {
        "Bucket": bucket_name,
        "Prefix": prefix,
    }

    if folders_only:
        # Makes S3 return immediate child prefixes in CommonPrefixes.
        request["Delimiter"] = "/"

    response = s3.list_objects_v2(**request)

    if folders_only:
        return [
            item["Prefix"]
            for item in response.get("CommonPrefixes", [])
        ]

    return [
        item["Key"]
        for item in response.get("Contents", [])
    ]



def s3_download_files(
    s3_source_path: str,
    local_dest_folder: Path,
    force: bool = False,
) -> None:
    """
    Download all objects under an S3 path to a local directory.

    Args:
        s3_source_path: Source path in the form
            ``s3://bucket-name/optional/prefix/``.
        local_dest_folder: Local directory where files are downloaded.
        force: If True, download files even when they already exist locally.

    Raises:
        ValueError: If ``s3_source_path`` is not a valid S3 URI.
    """
    if not s3_source_path.startswith("s3://"):
        raise ValueError(
            "s3_source_path must use the format "
            "'s3://bucket-name/optional/prefix/'."
        )

    bucket_name, _, prefix = s3_source_path.removeprefix("s3://").partition("/")
    if not bucket_name:
        raise ValueError("s3_source_path must include a bucket name.")

    if prefix and not prefix.endswith("/"):
        prefix += "/"

    local_dest_folder = Path(local_dest_folder)
    local_dest_folder.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client("s3")
    s3_paths = s3_ls(bucket_name, prefix)

    for s3_path in tqdm(s3_paths, desc="Downloading S3 files"):
        if s3_path.endswith("/"):
            continue

        # Retain subdirectories below the supplied source prefix.
        local_path = local_dest_folder / s3_path.removeprefix(prefix)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if local_path.exists() and not force:
            print(f"Skipping {local_path}; it already exists.")
            continue

        try:
            s3.download_file(bucket_name, s3_path, str(local_path))
        except ClientError as error:
            print(f"Failed to download s3://{bucket_name}/{s3_path}: {error}")



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
