from typing import Any

from credold.local_storage import LocalStorage
from credold.s3_storage import S3Storage


class Credold:
    def __init__(self, type_: str, params: dict[str, Any]) -> None:
        if type_ == "local":
            if "file_path" not in params:
                msg = "file_path is required"
                raise ValueError(msg)
            file_path = params["file_path"]
            self._storage = LocalStorage(file_path=file_path)
            return
        if type_ == "s3":
            if "bucket_name" not in params:
                msg = "bucket_name is required"
                raise ValueError(msg)
            bucket_name = params["bucket_name"]
            key = params.get("key", "credold.json")
            dir_ = params.get("dir")
            region_name = params.get("region_name")
            profile_name = params.get("profile_name")
            endpoint_url = params.get("endpoint_url")
            self._storage = S3Storage(
                bucket_name=bucket_name,
                key=key,
                dir_=dir_,
                region_name=region_name,
                profile_name=profile_name,
                endpoint_url=endpoint_url,
            )

    def save(self, data: dict) -> None:
        self._storage.save(data)

    def load(self) -> dict:
        return self._storage.load()

    @staticmethod
    def _localstack() -> "Credold":
        return Credold(
            type_="s3",
            params={
                "bucket_name": "credold-sample",
                "key": "credold.json",
                "dir": "tmp",
                "profile_name": "localstack",
                "region_name": "ap-northeast-1",
                "endpoint_url": "http://localhost:4567",
            },
        )


if __name__ == "__main__":
    # python -m src.credold
    credold = Credold._localstack()  # noqa: SLF001
    credold.save({"token": "dummy"})
    print(credold.load())
