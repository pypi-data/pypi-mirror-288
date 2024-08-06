# set up environment config
# set up task config
# utility to download file from s3 or from file system
# utility to update progress to stdout and optionally to CS/database
# utility to put the result somewhere (bucket/cs/filesystem)
from enum import Enum
import os
import dotenv
import json

import requests
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.client import Config as BotoConfig
from typing import Callable, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    UNKNOWN = 1
    STARTED = 2
    IN_PROGRESS = 3
    DONE = 4
    FAILED = 5


class Config:
    def __init__(self):
        if os.path.isfile(".env"):
            dotenv.load_dotenv(".env")
        self.in_cloud = os.environ.get("IN_CLOUD", False) in [
            "True",
            "true",
            "TRUE",
            "1",
        ]
        self.task_id = os.environ.get("TASK_ID")
        self.cloud_server_token = os.environ.get("CLOUD_SERVER_TOKEN")
        self.cloud_server_hostname = os.environ.get("CLOUD_SERVER_HOSTNAME")
        self.s3_bucket = os.environ.get("S3_BUCKET")
        self.s3_access_key_id = os.environ.get("S3_ACCESS_KEY_ID")
        self.s3_secret_access_key = os.environ.get("S3_SECRET_ACCESS_KEY")
        self.s3_region_name = os.environ.get("S3_REGION_NAME")
        self.s3_endpoint_url = os.environ.get(
            "S3_ENDPOINT_URL", "http://192.168.0.79:9000"
        )


class TaskRunner:
    def __init__(self, current_file_directory: str):
        self.config = Config()  # TODO: make this yaml
        self.work_dir = current_file_directory
        with open(self.work_dir + "/config/parameters.json") as f:
            self.parameters = json.load(f)
        if self.config.in_cloud:
            self.s3 = boto3.client(
                "s3",
                endpoint_url=self.config.s3_endpoint_url,
                aws_access_key_id=self.config.s3_access_key_id,
                aws_secret_access_key=self.config.s3_secret_access_key,
                config=BotoConfig(signature_version="s3v4"),
                region_name=self.config.s3_region_name,
            )
        else:
            self.s3 = None

    def update_status(
        self, status: TaskStatus, progress: float, details: str, result: dict = {}
    ):
        logger.info(
            f"---------\nSTATUS: {status}\nPROGRESS: {progress}\nDETAILS: {details}\nRESULT: {result}\n---------"
        )
        if self.config.in_cloud:
            # update progress in cloud server
            assert self.config.cloud_server_token
            headers = {"token": self.config.cloud_server_token}
            data = {
                "progress": progress,
                "status": status.value,
                "progress_details": details,
                "result": result,
            }
            r = requests.patch(
                f"{self.config.cloud_server_hostname}/tasks/api/v1/altb/compiler/{self.config.task_id}",
                headers=headers,
                json=data,
            )
            r.raise_for_status()

    def get_input_filepath(self):
        input_path = self.work_dir + "/data/inputs/input.file"
        if self.config.in_cloud:
            # Initialize a session using Amazon S3 with explicit credentials
            s3 = boto3.client(
                "s3",
                endpoint_url=self.config.s3_endpoint_url,
                aws_access_key_id=self.config.s3_access_key_id,
                aws_secret_access_key=self.config.s3_secret_access_key,
                config=BotoConfig(signature_version="s3v4"),
                region_name=self.config.s3_region_name,
            )

            try:
                # Download the file from S3
                logger.info(
                    f"Downloading file {self.config.task_id} from bucket {self.config.s3_bucket} to {input_path}"
                )
                s3.download_file(self.config.s3_bucket, self.config.task_id, input_path)
                logger.info(
                    f"File {self.config.task_id} downloaded successfully to {input_path}"
                )
            except NoCredentialsError:
                logger.info("Credentials not available")
                raise
            except PartialCredentialsError:
                logger.info("Incomplete credentials provided")
                raise
            except Exception as e:
                logger.info(f"Error downloading file: {e}")
                raise

        return input_path

    def upload_to_s3(self, result_path):
        if self.config.in_cloud:
            assert self.config.task_id
            try:
                # send to s3 bucket
                self.s3.upload_file(
                    str(result_path),
                    self.config.s3_bucket,
                    self.config.task_id + "_result",
                )
            except NoCredentialsError:
                logger.info("Credentials not available")
                raise
            except PartialCredentialsError:
                logger.info("Incomplete credentials provided")
                raise
            except Exception as e:
                logger.info(f"Error downloading file: {e}")
                raise
        else:
            pass

    def upload_to_cloud_server(self, result_path):
        if self.config.in_cloud:
            pass  # send to cloud server
        pass

    def run(
        self, callable: Callable[..., Any], tr: "TaskRunner", *args: Any, **kwargs: Any
    ) -> Optional[Any]:
        try:
            result = callable(tr, *args, **kwargs)
            return result
        except Exception as e:
            self.update_status(TaskStatus.FAILED, 0, f"An error occurred: {str(e)}")
            logger.error(f"An error occurred: {e}")
            return None

    def download_bucket(self, bucket_name, dst_dir):
        paths = []
        if self.config.in_cloud:
            # Create download path if it does not exist
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            # List objects in the S3 bucket
            objects = self.s3.list_objects_v2(Bucket=bucket_name)
            # Download each object
            for obj in objects.get("Contents", []):
                key = obj["Key"]
                file_path = os.path.join(dst_dir, key)

                # Create subdirectories if needed
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))

                self.s3.download_file(bucket_name, key, file_path)
                paths.append(file_path)
        else:
            for root, dirs, files in os.walk(dst_dir):
                for file in files:
                    paths.append(os.path.join(root, file))

        return paths
