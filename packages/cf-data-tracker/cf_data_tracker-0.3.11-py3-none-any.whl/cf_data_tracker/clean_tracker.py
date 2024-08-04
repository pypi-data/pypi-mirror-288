import json
import logging
import os
import re
import zipfile
from datetime import datetime
from functools import reduce
from typing import Any, List, Union

import boto3
from botocore.client import BaseClient
from dotenv import load_dotenv


# Configurations
load_dotenv()
AWS_REGION = "eu-west-2"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

# Logger setup
logger = logging.getLogger(__name__)


def create_session() -> boto3.session.Session:
    return boto3.session.Session(
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def create_client(service_name: str) -> BaseClient:
    session = create_session()
    return session.client(service_name)


def read_json_from_s3(bucket_name: str, json_key: str, s3_client: BaseClient) -> Any:
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=json_key)
    return json.loads(s3_object["Body"].read().decode("utf-8"))


def read_clean_version_json(bucket_name: str, json_key: str, schema_name: str) -> Any:
    s3_client = create_client("s3")
    try:
        return read_json_from_s3(bucket_name, json_key, s3_client)
    except s3_client.exceptions.NoSuchKey as e:
        return [{"schema_name": schema_name, "tables": {}}]


def write_parquet_to_s3(data, output_path: str, schema: str) -> None:
    if schema == "rtt":
        data = data.repartition(1)
    data.write.mode("append").parquet(output_path)


def write_file_to_s3(
    data: str, bucket_name: str, key: str, s3_client: BaseClient
) -> None:
    s3_client.put_object(Body=data, Bucket=bucket_name, Key=key)


def get_version_info(file_info: List[dict], version: int) -> Union[dict, None]:
    for item in file_info:
        if item["version"] == version:
            return item
    return None


def update_clean_version_info(
    version_info: dict,
    file_name: str,
    table_name: str,
    raw_file: str,
    version: int,
    output_prefix: str,
    modified_on: datetime,
) -> dict:
    file_info = {
        "file_info": {
            "raw_file": raw_file,
            "version": version,
            "table_name": table_name,
            "output_prefix": output_prefix,
            "modified_on": modified_on.strftime("%Y-%m-%d-%H-%M-%S"),
        }
    }
    version_info[0]["tables"][file_name] = file_info
    return version_info


def delete_parquet_files_boto3(
    bucket_name: str, prefix: str, s3_client: BaseClient
) -> None:
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        for content in page.get("Contents", []):
            file_path = content["Key"]
            if file_path.endswith(".parquet"):
                s3_client.delete_object(Bucket=bucket_name, Key=file_path)

    logger.info(f"Deleted the files starting with {prefix} successfully")


def does_s3_directory_exist(bucket: str, directory: str) -> bool:
    s3 = create_client("s3")
    result = s3.list_objects_v2(Bucket=bucket, Prefix=directory)
    return result["KeyCount"] > 0


def check_if_file_exists(bucket: str, key: str) -> bool:
    s3 = create_client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except s3.exceptions.ClientError:
        return False


def get_raw_and_clean_data_versions(
    schema_name: str, clean_bucket: str, raw_bucket: str = "vitalstatistix-raw"
):
    raw_version = read_json_from_s3(
        raw_bucket, f"{schema_name}/{schema_name}_version_info.json", s3_client
    )
    clean_version = read_clean_version_json(
        clean_bucket, f"{schema_name}/clean_version.json", schema_name
    )
    return raw_version, clean_version


def delete_old_parquet_files(s3_client, clean_s3_bucket, schema, table, file):
    logger.info(file["current_version"])
    logger.info(f"{schema}/{table['table_name']}/{file['file_name']}")
    delete_parquet_files_boto3(
        clean_s3_bucket,
        f"{schema}/{table['table_name']}/{file['file_name']}",
        s3_client,
    )


def get_existing_parquet_files(spark, clean_s3_bucket, schema, table):
    pass


def write_raw_data_to_s3(raw_data, clean_s3_bucket, schema, table):
    output_path = f"s3a://{clean_s3_bucket}/{schema}/{table['table_name']}"
    logger.info(f"Writing to {output_path}")
    print(f"Writing to {output_path}")
    write_parquet_to_s3(raw_data, output_path, schema)
    return output_path


def update_and_write_clean_version_info(
    schema: str,
    clean_bucket: str,
    clean_version,
    file,
    table,
    latest_version_info,
    new_parquet_files,
    s3_client,
):
    clean_version = update_clean_version_info(
        clean_version,
        file["file_name"],
        table["table_name"],
        latest_version_info["file"],
        file["current_version"],
        file["file_name"],
        datetime.now(),
    )

    clean_version[0]["tables"][file["file_name"]]["file_info"][
        "parquet_files"
    ] = new_parquet_files
    # writing the updated clean file to the s3
    write_file_to_s3(
        json.dumps(clean_version),
        f"{clean_bucket}",
        f"{schema}/clean_version.json",
        s3_client,
    )
