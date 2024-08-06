# set up environment config
# set up task config
# utility to download file from s3 or from file system
# utility to update progress to stdout and optionally to CS/database
# utility to put the result somewhere (bucket/cs/filesystem)
from enum import Enum
import os
import traceback
import dotenv
import json

import requests
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.client import Config as BotoConfig
from typing import Callable, Any
import logging
import signal
import multiprocessing

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    UNKNOWN = 1
    STARTED = 2
    IN_PROGRESS = 3
    DONE = 4
    FAILED = 5


EXIT_CODE_MESSAGES = {
    0: "Process completed successfully.",
    1: "Process terminated with a general error.",
    -signal.SIGTERM: "Process terminated by SIGTERM signal.",
    -signal.SIGKILL: "Process killed by SIGKILL signal.",
    -signal.SIGSEGV: "Process terminated by SIGSEGV (segmentation fault).",
}


# class ProcessRunner:
#     @staticmethod
#     def run_in_process(self, task_runner, func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):


#         return wrapper


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
        self.task_id = os.environ.get("TASK_ID", "")
        self.cloud_server_token = os.environ.get("CLOUD_SERVER_TOKEN", "")
        self.cloud_server_hostname = os.environ.get("CLOUD_SERVER_HOSTNAME", "")
        self.s3_bucket = os.environ.get("S3_BUCKET", "")
        self.s3_access_key_id = os.environ.get("S3_ACCESS_KEY_ID", "")
        self.s3_secret_access_key = os.environ.get("S3_SECRET_ACCESS_KEY", "")
        self.s3_region_name = os.environ.get("S3_REGION_NAME", "")
        self.s3_endpoint_url = os.environ.get(
            "S3_ENDPOINT_URL", "http://192.168.0.79:9000"
        )


class TaskRunner:
    def __init__(self, data_dir: str, config_dir: str):
        # self.process_runner = ProcessRunner()
        self.config = Config()  # TODO: make this yaml
        self.data_dir = data_dir
        self.config_dir = config_dir
        with open(self.config_dir + "/parameters.json") as f:
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
                "result": json.dumps(result),
            }
            r = requests.patch(
                f"{self.config.cloud_server_hostname}/tasks/api/v1/altb/compiler/{self.config.task_id}",
                headers=headers,
                json=data,
            )
            r.raise_for_status()

    def get_input_filepath(self):
        input_path = self.data_dir + "/data/inputs/input.file"
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

    def upload_outputs(self, output_dir):
        if self.config.in_cloud:
            try:
                # send to s3 bucket
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        self.s3.upload_file(
                            os.path.join(root, file),
                            self.config.s3_bucket,
                            self.config.task_id + "/outputs/" + file,
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

    # def run_in_process(self, func):
    #     return ProcessRunner.run_in_process(self, func)

    def run(
        self, func: Callable[..., Any], tr: "TaskRunner", *args: Any, **kwargs: Any
    ) -> None:

        parent_conn, child_conn = multiprocessing.Pipe()
        # try:
        #     result = callable(tr, *args, **kwargs)
        #     return result
        # except Exception as e:
        #     self.update_status(TaskStatus.FAILED, 0, "An error occurred", str(e))
        #     logger.error(f"An error occurred: {e}")
        #     return None

        def process_target(conn, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
                conn.send((0, None, None))  # Send success status
            except Exception as e:
                self.update_status(
                    TaskStatus.FAILED,
                    0,
                    "An error occurred",
                    {"result": "FAILED", "error": str(e)},
                )
                logger.error(f"An error occurred: {e}")
                tb = traceback.format_exc()
                conn.send((1, str(e), tb))  # Send error status and traceback

        process = multiprocessing.Process(
            target=process_target, args=(child_conn, *args), kwargs=kwargs
        )
        process.start()
        process.join()  # Wait for the process to finish

        # Retrieve exit code and diagnostic information
        if parent_conn.poll():
            status, error_msg, tb = parent_conn.recv()
            if status == 0:
                logger.info(f"Process for {func.__name__} completed successfully.")
            else:
                self.update_status(
                    TaskStatus.FAILED,
                    0,
                    "An error occurred",
                    {"result": "FAILED", "error": error_msg, "traceback": tb},
                )
                logger.info(
                    f"Process for {func.__name__} exited with an error: {error_msg}\nTraceback:\n{tb}"
                )
        else:
            exit_code = process.exitcode
            self.update_status(
                TaskStatus.FAILED,
                0,
                "An error occurred",
                {"result": "FAILED", "error_code": exit_code},
            )
            if exit_code in EXIT_CODE_MESSAGES:
                logger.info(
                    f"Process for {func.__name__} exited with code {exit_code}: {EXIT_CODE_MESSAGES[exit_code]}"
                )
            else:
                logger.info(
                    f"Process for {func.__name__} exited with an unknown error code {exit_code}."
                )

    def download_bucket(self, bucket_name, dst_dir):
        paths = []
        if self.config.in_cloud:
            # Create download path if it does not exist
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            # List objects in the S3 bucket
            objects = self.s3.list_objects_v2(
                Bucket=bucket_name, Prefix=self.config.task_id + "/inputs/"
            )
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

    def download_inputs(self, dst_dir):
        downloaded_files = []
        if self.config.in_cloud:
            # Create download path if it does not exist
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            # List objects in the S3 bucket
            objects = self.s3.list_objects_v2(
                Bucket=self.config.s3_bucket, Prefix=self.config.task_id + "/inputs/"
            )
            # Download each object
            for obj in objects.get("Contents", []):
                key = obj["Key"]
                file_path = os.path.join(dst_dir, key)

                # Create subdirectories if needed
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))

                self.s3.download_file(
                    self.config.s3_bucket, key, os.path.basename(file_path)
                )
                downloaded_files.append(file_path)
        else:
            for root, dirs, files in os.walk(dst_dir):
                for file in files:
                    downloaded_files.append(file)

        return downloaded_files
