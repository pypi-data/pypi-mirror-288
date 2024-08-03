# order_key = upload_document(order_path)
# result = get_extraction_result(order_key)
# output = load_result_from_s3(result)

import logging
import boto3
import json
import pathlib
import hashlib
from botocore.exceptions import ClientError
import urllib.parse
import requests
import itertools


def _get_hash_from_bytes(content: bytes):
    hash_object = hashlib.sha256()
    hash_object.update(content)
    hash_id = hash_object.hexdigest()
    return hash_id


def _upload_document(content: bytes, s3_bucket: str):
    hash_id = _get_hash_from_bytes(content)
    s3 = boto3.client("s3")
    key = f"input-order-documents/{hash_id}"
    # check if file exists
    try:
        _ = s3.head_object(Bucket=s3_bucket, Key=key)
        logging.info(
            "Content already exists:\n'%s/%s'\n(filename is hash of file content)",
            s3_bucket,
            key,
        )

    except ClientError:
        logging.info("File does not exist in bucket, uploading file")
        s3.put_object(Bucket=s3_bucket, Key=key, Body=content)

    return key


def _get_extraction_result(key: str, lambda_function_name: str):
    lambda_client = boto3.client("lambda")
    payload = json.dumps({"source_key": key})

    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType="RequestResponse",
        Payload=payload,
    )
    response_payload = response["Payload"].read()
    response_payload = json.loads(response_payload)
    return response_payload


def _get_comparison_result(order_key: str, offer_id: str, lambda_function_name: str):
    lambda_client = boto3.client("lambda")
    payload = json.dumps({"order_json_key": order_key, "offer_id": offer_id})
    print(f"payload={payload}")

    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType="RequestResponse",
        Payload=payload,
    )
    response_payload = response["Payload"].read()
    response_payload = json.loads(response_payload)
    return response_payload


def _load_extraction_result_from_s3(
    result_obj, s3_bucket, parts=("positions", "header"), formats=("html", "json")
):
    if not (result_obj["body"] == "Success" and result_obj["statusCode"] == 200):
        raise ValueError(f"Error in lambda function: {result_obj}")
    s3 = boto3.client("s3")
    output = dict()
    for part in parts:
        for format_value in formats:
            object_key = f"{part}_{format_value}"
            logging.info("Loading %s from s3", object_key)
            if not object_key in result_obj:
                continue
            uri = result_obj[object_key]
            key = uri.split("mi-order-extraction-service/")[-1]
            obj = s3.get_object(Bucket=s3_bucket, Key=key)
            output[object_key] = obj["Body"].read().decode("utf-8")
    logging.info("result successfully loaded from s3")
    return output


def _load_comparison_result_from_s3(result_obj, s3_bucket):
    if not (result_obj["body"] == "Success" and result_obj["statusCode"] == 200):
        raise ValueError(f"Error in lambda function: {result_obj}")

    s3_uri = result_obj["comparison_html_uri"]
    # Parse the S3 URI

    s3_parts = s3_uri.replace("s3://", "").split("/")
    bucket_name = s3_parts.pop(0)
    key = "/".join(s3_parts)

    # Initialize a session using Amazon S3
    s3 = boto3.client("s3")

    # Download the file
    response = s3.get_object(Bucket=bucket_name, Key=key)

    # Read the content of the file
    content = response["Body"].read().decode("utf-8")
    return content


class GetContentException(Exception):

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def _get_content(order_path: str | pathlib.Path):
    # check if order_path is url
    is_url = False
    if isinstance(order_path, str):
        try:
            result = urllib.parse.urlparse(order_path)
            if all([result.scheme, result.netloc, result.path]):
                logging.info("URL found: %s", order_path)
                is_url = True

        except ValueError:
            logging.info("Path found: %s", order_path)
            is_url = False

    if is_url:
        # download the file from the url
        response = requests.get(order_path)
        # check if the request was successful
        if not response.ok:
            raise GetContentException(
                f"Error downloading file from {order_path}", response.status_code
            )

        # read the content of the file
        content = response.content
        logging.info("Downloaded file from %s", order_path)
    else:
        # file is a local path
        path = pathlib.Path(order_path)
        if not path.exists():
            raise ValueError(f"File {order_path} does not exist")

        if not path.is_file():
            raise ValueError(f"Path {order_path} is not a file")

        content = path.read_bytes()

    return content


class Client:

    def __init__(self, bucket_name, lambda_name, lambda_comparison_name=None):
        self.bucket_name = bucket_name
        self.lambda_name = lambda_name
        self.lambda_comparison_name = lambda_comparison_name

    def get_content(self, order_path: str | pathlib.Path):
        try:
            content = _get_content(order_path)
            return content, None
        except Exception as e:
            if isinstance(e, GetContentException):
                message = f"couldn't get the content from the provided url. The return statuscode was {e.status_code}"
            else:
                message = (
                    f"couldn't get the content from the provided url. The error was {e}"
                )
            return None, {"message": message, "status_code": 401}

    def upload_to_s3(self, content: bytes):
        try:
            order_key = _upload_document(content, self.bucket_name)
            logging.info("Document uploaded to s3. Key: %s", order_key)
            return order_key, None
        except Exception as e:
            return None, {
                "message": f"couldn't upload the document to s3. The error was {e}",
                "status_code": 401,
            }

    def get_extraction_result(self, order_key: str):
        try:
            result = _get_extraction_result(order_key, self.lambda_name)
            if not ("statusCode" in result and result["statusCode"] == 200):
                raise ValueError(f"Error in lambda function: {result}")
            logging.info("Extraction result: %s", result)
            return result, None
        except Exception as e:
            return None, {
                "message": f"couldn't get the extraction result from the lambda function. The error was {e}",
                "status_code": 401,
            }

    def get_comarison_result(self, order_json_key: str, offer_id: str):
        print(f"order_json_key={order_json_key}")
        print(f"offer_id={offer_id}")
        try:
            result = _get_comparison_result(
                order_json_key, offer_id, self.lambda_comparison_name
            )
            if not ("statusCode" in result and result["statusCode"] == 200):
                raise ValueError(f"Error in lambda function: {result}")
            logging.info("Comparison result: %s", result)
            return result, None
        except Exception as e:
            return None, {
                "message": f"couldn't get the comparison result from the lambda function. The error was {e}",
                "status_code": 401,
            }

    def get_order_key(self, result_obj):
        try:
            if not ("statusCode" in result_obj and result_obj["statusCode"] == 200):
                return None, {
                    "message": f"Error in lambda function: {result_obj}",
                    "status_code": 401,
                }
            key = "positions_json"
            if key not in result_obj:
                return None, {
                    "message": f"couldn't get the order key from the result. The key {key} was not found",
                    "status_code": 401,
                }
            s3_uri = result_obj[key]
            # Parse the S3 URI and get the s3_key
            s3_parts = s3_uri.replace("s3://", "").split("/")
            bucket_name = s3_parts.pop(0)
            key = "/".join(s3_parts)

            return key, None
        except Exception as e:
            return None, {
                "message": f"couldn't get the order key from the result. The error was {e}",
                "status_code": 401,
            }

    def load_comparison_result(self, result_obj):
        try:
            html = _load_comparison_result_from_s3(result_obj, self.bucket_name)
            logging.info("html: %s", html)
            return html, None
        except Exception as e:
            return None, {
                "message": f"couldn't load the comparison result from s3. The error was {e}",
                "status_code": 401,
            }

    def compare(self, order_path: str | pathlib.Path, offer_id: str):
        if not self.lambda_comparison_name:
            return {
                "message": "Comparison not supported. Please provide the lambda_comparison_name in the constructor!",
                "status_code": 401,
            }
        content, err = self.get_content(order_path)
        if err:
            return err
        order_key, err = self.upload_to_s3(content)
        if err:
            return err
        # here run extraction
        ext_res, err = self.get_extraction_result(order_key)
        if err:
            return err

        order_key, err = self.get_order_key(ext_res)
        if err:
            return err

        print(f"order_key={order_key}")

        comp_res, err = self.get_comarison_result(order_key, offer_id)
        if err:
            return err

        html, err = self.load_comparison_result(comp_res)
        if err:
            return err

        return {"message": "Comparison successful", "status_code": 200, "content": html}

    def extract(
        self, order_path: str | pathlib.Path, parts=("positions",), formats=("html",)
    ):
        # check if parts and are tuples
        if not isinstance(parts, tuple):
            raise ValueError("parts must be a tuple")
        if not isinstance(formats, tuple):
            raise ValueError("formats must be a tuple")

        # check if parts and formats are valid
        for part in parts:
            if part not in ("positions", "header"):
                raise ValueError(f"Invalid part: {part}")

        for format_value in formats:
            if format_value not in ("html", "json"):
                raise ValueError(f"Invalid format: {format_value}")

        ########################################
        try:
            content = _get_content(order_path)
        except Exception as e:
            if isinstance(e, GetContentException):
                message = f"couldn't get the content from the provided url. The return statuscode was {e.status_code}"
            else:
                message = (
                    f"couldn't get the content from the provided url. The error was {e}"
                )
            return {"message": message, "status_code": 401}

        ########################################
        try:
            order_key = _upload_document(content, self.bucket_name)
            logging.info("Document uploaded to s3. Key: %s", order_key)
        except Exception as e:
            return {
                "message": f"couldn't upload the document to s3. The error was {e}",
                "status_code": 401,
            }

        ########################################
        try:
            result = _get_extraction_result(order_key, self.lambda_name)
            if not ("statusCode" in result and result["statusCode"] == 200):
                raise ValueError(f"Error in lambda function: {result}")
            logging.info("Extraction result: %s", result)
        except Exception as e:
            return {
                "message": f"couldn't get the extraction result from the lambda function. The error was {e}",
                "status_code": 401,
            }

        ########################################
        try:
            output = _load_extraction_result_from_s3(
                result, self.bucket_name, parts=parts, formats=formats
            )
            logging.info("Output: %s", output)
            object_keys = [f"{p}_{f}" for p, f in itertools.product(parts, formats)]
            for key in object_keys:
                if key not in output:
                    return {
                        "message": f"couldn't load the result from s3. The key {key} was not found",
                        "status_code": 401,
                    }
            
            if len(object_keys) == 1:
                content = output[object_keys[0]]
                return {
                    "message": "Extraction successful",
                    "status_code": 200,
                    "content": content,
                }
            else:
                return {
                    "message": "Extraction successful",
                    "status_code": 200,
                    "content": output,
                }
        except Exception as e:
            return {
                "message": f"couldn't load the result from s3. The error was '{e}'",
                "status_code": 401,
            }
