import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from storage import Storage


def _get_client(region_name: str | None = None, endpoint_url: str | None = None):  # noqa: ANN202
    s3_client_params = {"service_name": "s3"}
    if region_name:
        s3_client_params["region_name"] = region_name
    if endpoint_url:
        s3_client_params["endpoint_url"] = endpoint_url
    return boto3.client(**s3_client_params)


class S3Storage(Storage):
    def __init__(
        self,
        bucket_name: str,
        key: str = "s3_storage.json",
        dir_: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
        endpoint_url: str | None = None,
    ) -> None:
        if profile_name:
            boto3.setup_default_session(profile_name=profile_name)
        self._s3_client = _get_client(region_name=region_name, endpoint_url=endpoint_url)
        self._key = key
        self._dir = dir_
        self._bucket_name = bucket_name

    @staticmethod
    def localstack(
        bucket_name: str,
        key: str = "s3_storage.json",
        dir_: str | None = None,
    ) -> "S3Storage":
        return S3Storage(
            bucket_name=bucket_name,
            key=key,
            dir_=dir_,
            profile_name="localstack",
            region_name="ap-northeast-1",
            endpoint_url="http://localhost:4567",
        )

    def save(self, data: dict) -> None:
        path = self._path()
        try:
            with path.open(mode="w") as f:
                json.dump(data, f, indent=4)
            self._s3_client.upload_file(path.resolve(), self._bucket_name, path.name)
        finally:
            path.unlink()

    def load(self) -> dict:
        path = self._path()
        try:
            self._s3_client.download_file(
                self._bucket_name,
                path.name,
                path.resolve(),
            )
            with path.open() as f:
                return json.load(f)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                msg = f"FileNotFound: bucket_name: {self._bucket_name}, file_path: {path.name}"
                raise FileNotFoundError(msg) from e
            raise e
        except:
            raise

    def _path(self) -> Path:
        if self._dir:
            dir_ = self._dir if self._dir.startswith("/") else f"/{self._dir}"
            return Path(dir_) / self._key
        return Path(self._key)
