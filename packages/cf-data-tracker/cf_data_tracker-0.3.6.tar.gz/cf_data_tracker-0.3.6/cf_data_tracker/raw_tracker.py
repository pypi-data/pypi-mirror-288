import json
from typing import Any, Dict, List
from datetime import datetime
import json
import os
from typing import Any, Dict, List
from .utils import S3_CLIENT
import re
import requests
import boto3
from typing import Dict, Any


s3 = S3_CLIENT

def version_file_path(schema_name: str) -> str:
    """Get the path to the version info file for a schema.

    Args:
        schema_name: The name of the schema.

    Returns:
        The path to the version info file for the schema.

    """
    return f"{schema_name}/{schema_name}_version_info.json"


def read_version_file(schema: str, s3=S3_CLIENT) -> List[Dict[str, int]]:
    """
    The `read_version_file` function reads the version info file for a given schema from an Amazon S3 bucket. If the file exists, it is returned as a list of dictionaries representing the version information for each table and file in the schema. If the file does not exist, an empty list is returned. # noqa: E501

    Args:
        - `schema`: The name of the schema to read the version info file for.

    Returns:
        - A list of dictionaries representing the version information for each table and file in the schema. If the file does not exist, an empty list is returned.
    """
    bucket: str = os.environ["AWS_DEST_BUCKET_RAW"]
    file_key: str = f"{schema}/{schema}_version_info.json"
    print(
        f"Reading version info file for {schema} from S3 bucket {bucket} at {file_key}"
    )
    # Get the version info from S3
    try:
        response: Dict[str, Any] = s3.get_object(Bucket=bucket, Key=file_key)
        version_info_str: str = response["Body"].read().decode("utf-8")
        version_info: List[Dict[str, int]] = json.loads(version_info_str)
    except s3.exceptions.NoSuchKey:
        # If the file does not exist, create an empty version info structure
        version_info: Dict[str, List[Dict[str, int]]] = {"tables": [{"schema_name": schema, "tables": []}]}
    
    return version_info

def update_version_info(
    version_info: Dict,
    schema: str,
    table: str,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    # Update the version info dictionary with the file information.
    """
    Updates the version information for a file in a given schema and table.

    Args:
        - `version_info` (Dict): The current version information for the schema.
        - `schema` (str): The name of the schema.
        - `table` (str): The name of the table.
        - `file_name` (str): The name of the file.
        - `file` (str): The file itself.
        - `file_size` (int): The size of the file in bytes.
        - `timestamp` (str): The timestamp of the file.

    Returns:
        - Dict: The updated version information for the schema, with the new file version and information added.
    """
    # Update the version info dictionary with the file information.
    schema_entry = get_schema_entry(version_info, schema)
    table_entry = get_table_entry(schema_entry, table)
    file_entry = update_file_entry(
        table_entry,
        file_name,
        file,
        file_size,
        s3_location,
        timestamp,
        fyear,
        upload_date,
    )  # noqa: F841, E231, E261, E501
    updated_table_entry = update_table_entry_for_the_file_with_updated_file_entry(
        table_name=table,
        file_name=file_name,
        file_entry=file_entry,
        table_entry=table_entry,
    )  # noqa: F841, E231, E261, E501
    version_info_updated = update_table_entry_of_version_info(
        version_info=version_info,
        updated_table_entry=updated_table_entry,
        table_name=table,
        schema_name=schema,
    )
    return version_info_updated


def write_version_file(schema_name: str, version_data: dict) -> None:
    """Uploads the schema version file to Amazon S3.

    Args:
        schema_name: The name of the schema.
        version_data: A dictionary of the schema version data.
    """
    try:
        bucket = os.environ["AWS_DEST_BUCKET_RAW"]
        key = f"{version_file_path(schema_name)}"
        body = json.dumps(version_data)

        print(f"Uploading version file to: s3://{bucket}/{key}")
        s3.put_object(Body=body, Bucket=bucket, Key=key)
        print("Successfully uploaded version file.")
    except Exception as e:
        print(f"Failed to upload version file: {e}")




def initialize_version_file(file_path, s3_client):  # Add s3_client parameter here
    """This function initializes a version file. It takes a file path and an s3 client and returns nothing.

    The file path is the path to the file in the S3 bucket. The s3 client is the boto3 client that connects to S3.
    """
    version_info = {"tables": []}
    s3_client.put_object(
        Bucket=os.environ["AWS_DEST_BUCKET_RAW"],
        Key=version_file_path(file_path),
        Body=json.dumps(version_info),
    )


def update_table_entry_of_version_info(
    version_info: Dict, updated_table_entry: Dict, table_name: str, schema_name: str
) -> Dict:
    updated_version_info = {"tables": [{"schema_name": schema_name, "tables": []}]}
    for table in version_info["tables"][0]["tables"]:
        if table["table_name"] == table_name:
            updated_version_info["tables"][0]["tables"].append(updated_table_entry)
        else:
            updated_version_info["tables"][0]["tables"].append(table)
    return updated_version_info


def update_version_info(
    version_info: Dict,
    schema: str,
    table: str,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    # Update the version info dictionary with the file information.
    """
    Updates the version information for a file in a given schema and table.

    Args:
        - `version_info` (Dict): The current version information for the schema.
        - `schema` (str): The name of the schema.
        - `table` (str): The name of the table.
        - `file_name` (str): The name of the file.
        - `file` (str): The file itself.
        - `file_size` (int): The size of the file in bytes.
        - `timestamp` (str): The timestamp of the file.

    Returns:
        - Dict: The updated version information for the schema, with the new file version and information added.
    """
    # Update the version info dictionary with the file information.
    schema_entry = get_schema_entry(version_info, schema)
    table_entry = get_table_entry(schema_entry, table)
    file_entry = update_file_entry(
        table_entry,
        file_name,
        file,
        file_size,
        s3_location,
        timestamp,
        fyear,
        upload_date,
    )  # noqa: F841, E231, E261, E501
    updated_table_entry = update_table_entry_for_the_file_with_updated_file_entry(
        table_name=table,
        file_name=file_name,
        file_entry=file_entry,
        table_entry=table_entry,
    )  # noqa: F841, E231, E261, E501
    version_info_updated = update_table_entry_of_version_info(
        version_info=version_info,
        updated_table_entry=updated_table_entry,
        table_name=table,
        schema_name=schema,
    )
    return version_info_updated


def get_schema_entry(version_info: Dict, schema: str) -> Dict:
    """
        Gets the schema entry from the version information for the given schema. If the schema does not exist in the version information, a new schema entry is created with an empty list of tables. # noqa: E501

    Args:
        - `version_info` (Dict): The current version information for the schema.
        - `schema` (str): The name of the schema.

        Returns:
        - Dict: The schema entry from the version information for the given schema. If the schema does not exist in the version information, a new schema entry is created with an empty list of tables.
    """
    schema_entry = next(
        (entry for entry in version_info["tables"] if entry["schema_name"] == schema),
        None,
    )

    # If schema_entry is None, create a new schema entry and add it to version_info
    if not schema_entry:
        schema_entry = {"schema_name": schema, "tables": []}
        version_info["tables"].append(schema_entry)

    return schema_entry


def get_table_entry(schema_entry: Dict, table: str) -> Dict:
    """
    Gets the table entry from the schema entry for the given table. If the table
    does not exist in the schema entry, a new table entry is created with an
    empty list of files and added to the schema entry.

    Args:
        schema_entry (Dict): The schema entry containing the table information.
        table (str): The name of the table to get the entry for.

    Returns:
        Dict: The table entry from the schema entry for the given table. If the
              table does not exist in the schema entry, a new table entry is
              created with an empty list of files and added to the schema entry.
    """
    table_entry = next(
        (entry for entry in schema_entry["tables"] if entry["table_name"] == table),
        None,
    )

    # If table_entry is None, create a new table entry and add it to schema_entry
    if not table_entry:
        table_entry = {"table_name": table, "files": []}
        schema_entry["tables"].append(table_entry)

    return table_entry


def get_file_entry(
    table_entry: Dict, file_name: str, file: str, file_size: int, timestamp: str
) -> Dict:
    """
    Gets the file entry from the table entry for the given file_name. If the file_name
    does not exist in the table entry, a new file entry is created with version 1 and
    the provided file information, then added to the table entry.

    Args:
        table_entry (Dict): The table entry containing the file information.
        file_name (str): The name of the file to get the entry for.
        file (str): The file itself.
        file_size (int): The size of the file in bytes.
        timestamp (str): The timestamp of the file.

    Returns:
        Dict: The file entry from the table entry for the given file_name. If the
              file_name does not exist in the table entry, a new file entry is
              created with version 1 and the provided file information, then added
              to the table entry.
    """
    file_entry = next(
        (entry for entry in table_entry["files"] if entry["file_name"] == file_name),
        None,
    )

    # If file_entry is None, create a new file entry with version 1 and add it to table_entry
    if not file_entry:
        file_entry = {
            "file_name": file_name,
            "current_version": 1,
            "versions": [
                {
                    "version": 1,
                    "timestamp": timestamp,
                    "file_size": file_size,
                    "file": file,
                },
            ],
        }
        table_entry["files"].append(file_entry)

    return file_entry


def update_file_entry(
    table_entry: Dict,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    # Find the file_entry for the file corresponding to the given file_name.
    file_entry = next(
        (entry for entry in table_entry["files"] if entry["file_name"] == file_name),
        None,
    )

    # If file_entry is None, create a new file entry with version 1 and add it to table_entry
    if not file_entry:
        file_entry = {
            "file_name": file_name,
            "current_version": 1,
            "versions": [
                {
                    "version": 1,
                    "timestamp": timestamp,
                    "file_size": file_size,
                    "file": file,
                    "s3_location": s3_location,
                    "fyear": fyear,
                    "upload_date": upload_date,
                },
            ],
        }
        table_entry["files"].append(file_entry)
    else:
        # Increment the current_version of the file
        file_entry["current_version"] += 1

        # Add a new version entry to the file_entry's versions list
        new_version = {
            "version": file_entry["current_version"],
            "timestamp": timestamp,
            "file_size": file_size,
            "file": file,
            "s3_location": s3_location,
            "fyear": fyear,
            "upload_date": upload_date,
        }
        file_entry["versions"].append(new_version)

    return file_entry


def update_table_entry_for_the_file_with_updated_file_entry(
    table_name, file_name, file_entry, table_entry
):
    updated_table_entry = {"table_name": table_name, "files": []}
    for fe in table_entry["files"]:
        if fe["file_name"] == file_name:
            updated_table_entry["files"].append(file_entry)
        else:
            updated_table_entry["files"].append(fe)
    return updated_table_entry


def write_version_file(schema_name: str, version_data: dict) -> None:
    """Uploads the schema version file to Amazon S3.

    Args:
        schema_name: The name of the schema.
        version_data: A dictionary of the schema version data.
    """
    try:
        bucket = os.environ["AWS_DEST_BUCKET_RAW"]
        key = f"{version_file_path(schema_name)}"
        body = json.dumps(version_data)

        print(f"Uploading version file to: s3://{bucket}/{key}")
        s3.put_object(Body=body, Bucket=bucket, Key=key)
        print("Successfully uploaded version file.")
    except Exception as e:
        print(f"Failed to upload version file: {e}")






def display_bucket_contents(
    bucket_name: str = "vitalstatistix-raw-dev", s3_client=s3
) -> None:
    """
    Displays the contents of the specified S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket to display the contents of.
        s3_client: The S3 client to use for accessing the bucket (default: s3).
    """
    try:
        # List the objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check if there are any objects in the bucket
        if "Contents" not in response:

            print(f"No objects found in the bucket '{bucket_name}'.")
            return

        # Print the contents of the bucket
        print(f"Contents of the bucket '{bucket_name}':")
        res = []
        for obj in response["Contents"]:
            if "HES_" in obj["Key"]:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
                res.append(
                    {"file": f"{obj['Key'].split('/')[-1]}", "size": obj["Size"]}
                )
            #     pass
            # else:
            #     res.append(
            #         {"file": f"{obj['Key'].split('/')[-1]}", "size": obj["Size"]}
            #     )
        return res

    except Exception as e:
        print(f"Failed to display bucket contents: {e}")


def update_file_info(
    table_name: str,
    file: str,
    file_name: str,
    schema_name: str,
    file_size: int,
    s3_location: str,
    timestamp: str = None,
    fyear: str = None,
    upload_date: str = None,
) -> None:
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d")
    version_info = read_version_file(schema_name)

    version_info = update_version_info(
        version_info,
        schema_name,
        table_name,
        file,
        file_name,
        file_size,
        s3_location,
        timestamp,
        fyear,
        upload_date,
    )
    write_version_file(schema_name, version_info)

def upload_to_s3(file_path: str, bucket_name: str, s3_key: str) -> None:
    """Uploads a file to S3."""
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"Uploaded: {file_path} to s3://{bucket_name}/{s3_key}")

def update_version_tracker(schema_name: str, table_name: str, file_name: str, file_size: int, s3_location: str) -> None:
    """Updates the version tracker with the new file information."""
    version_info = read_version_file(schema_name)
    update_file_info(
        table_name=table_name,
        file=file_name,
        file_name=file_name,
        schema_name=schema_name,
        file_size=file_size,
        s3_location=s3_location,
    )
    write_version_file(schema_name, version_info)
    print(f"Updated version tracker for: {file_name}")


