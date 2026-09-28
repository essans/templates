import json
import os
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError
#from tqdm import tqdm
from tqdm.autonotebook import tqdm

from .aws_utils import get_aws_secret


def get_r2_client(account_id: str | None = None) -> Any:
    """Build a boto3 client pointed at Cloudflare R2's S3-compatible endpoint."""
    account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
    if not account_id:
        raise ValueError("account_id must be provided or set via CLOUDFLARE_ACCOUNT_ID.")

    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        raise ValueError("R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY must be set.")

    return boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )


def set_r2_credentials(secret_name: str, region: str) -> Any:
    """Fetch R2 credentials (JSON: account_id, access_key_id, secret_access_key) from AWS Secrets Manager."""
    try:
        secret_val = get_aws_secret(secret_name, region)

        if secret_val:
            creds = json.loads(secret_val)
            os.environ["CLOUDFLARE_ACCOUNT_ID"] = creds["account_id"]
            os.environ["R2_ACCESS_KEY_ID"] = creds["access_key_id"]
            os.environ["R2_SECRET_ACCESS_KEY"] = creds["secret_access_key"]
            print("R2 credentials set from AWS Secrets Manager.")
        else:
            print(f"Warning: could not fetch secret {secret_name} from AWS Secrets Manager.")
    except Exception as e:
        print(f"R2 credentials setup failed: {e}")


def r2_buckets() -> list[str]:
    r2 = get_r2_client()
    response = r2.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])]


def r2_ls(bucket_name: str, prefix: str = "") -> list[str]:
    """
    List the contents (keys) of an R2 bucket.
    Args:
        bucket_name (str): Name of the R2 bucket.
        prefix (str): Optional prefix to filter objects.
    Returns:
        List[str]: List of object keys in the bucket.
    """
    r2 = get_r2_client()
    paginator = r2.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys


def r2_ls2(bucket_name: str, prefix: str = "", folders_only: bool = False) -> list[str]:
    """List R2 objects or virtual folders beneath an optional prefix."""
    r2 = get_r2_client()

    request = {
        "Bucket": bucket_name,
        "Prefix": prefix,
    }

    if folders_only:
        # Makes R2 return immediate child prefixes in CommonPrefixes.
        request["Delimiter"] = "/"

    response = r2.list_objects_v2(**request)

    if folders_only:
        return [
            item["Prefix"]
            for item in response.get("CommonPrefixes", [])
        ]

    return [
        item["Key"]
        for item in response.get("Contents", [])
    ]


def r2_download_files(
    r2_source_path: str,
    local_dest_folder: Path,
    force: bool = False,
) -> None:
    """
    Download all objects under an R2 path to a local directory.

    Args:
        r2_source_path: Source path in the form
            ``r2://bucket-name/optional/prefix/``.
        local_dest_folder: Local directory where files are downloaded.
        force: If True, download files even when they already exist locally.

    Raises:
        ValueError: If ``r2_source_path`` is not a valid R2 URI.
    """
    if not r2_source_path.startswith("r2://"):
        raise ValueError(
            "r2_source_path must use the format "
            "'r2://bucket-name/optional/prefix/'."
        )

    bucket_name, _, prefix = r2_source_path.removeprefix("r2://").partition("/")
    if not bucket_name:
        raise ValueError("r2_source_path must include a bucket name.")

    if prefix and not prefix.endswith("/"):
        prefix += "/"

    local_dest_folder = Path(local_dest_folder)
    local_dest_folder.mkdir(parents=True, exist_ok=True)

    r2 = get_r2_client()
    r2_paths = r2_ls(bucket_name, prefix)

    for r2_path in tqdm(r2_paths, desc="Downloading R2 files"):
        if r2_path.endswith("/"):
            continue

        # Retain subdirectories below the supplied source prefix.
        local_path = local_dest_folder / r2_path.removeprefix(prefix)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if local_path.exists() and not force:
            print(f"Skipping {local_path}; it already exists.")
            continue

        try:
            r2.download_file(bucket_name, r2_path, str(local_path))
        except ClientError as error:
            print(f"Failed to download r2://{bucket_name}/{r2_path}: {error}")


def upload_directory_to_r2(local_dir: str, bucket_name: str, r2_prefix: str = "") -> None:
    """
    Upload all files from a local directory to a specified R2 bucket path.
    Args:
        local_dir (str): Path to the local directory to upload.
        bucket_name (str): Name of the R2 bucket.
        r2_prefix (str): R2 prefix (folder path in the bucket) to upload files to.
    """
    r2_client = get_r2_client()
    local_dir = os.path.abspath(local_dir)
    if not os.path.isdir(local_dir):
        raise ValueError(f"{local_dir} is not a valid directory.")
    # Walk through local_dir and upload each file
    files_to_upload = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            full_path = os.path.join(root, file)
            # R2 key: prefix + relative path from local_dir
            rel_path = os.path.relpath(full_path, local_dir)
            r2_key = os.path.join(r2_prefix, rel_path).replace("\\", "/")
            files_to_upload.append((full_path, r2_key))
    for full_path, r2_key in tqdm(files_to_upload, desc="Uploading to R2"):
        try:
            r2_client.upload_file(full_path, bucket_name, r2_key)
            print(f"Uploaded {full_path} to r2://{bucket_name}/{r2_key}")
        except Exception as e:
            print(f"Failed to upload {full_path} to {r2_key}: {e}")


def upload_file_to_r2(local_file_path: str, bucket_name: str, r2_prefix: str = "") -> None:
    """
    Upload a single file to a specified R2 bucket and prefix, preserving the file name.
    Args:
        local_file_path (str): Path to the local file to upload.
        bucket_name (str): Name of the R2 bucket.
        r2_prefix (str): R2 prefix (folder path in the bucket) to upload the file to.
    """
    r2_client = get_r2_client()
    if not os.path.isfile(local_file_path):
        raise ValueError(f"{local_file_path} is not a valid file.")
    file_name = os.path.basename(local_file_path)
    r2_key = os.path.join(r2_prefix, file_name).replace("\\", "/") if r2_prefix else file_name
    try:
        r2_client.upload_file(local_file_path, bucket_name, r2_key)
        print(f"Uploaded {local_file_path} to r2://{bucket_name}/{r2_key}")
    except Exception as e:
        print(f"Failed to upload {local_file_path} to {r2_key}: {e}")
