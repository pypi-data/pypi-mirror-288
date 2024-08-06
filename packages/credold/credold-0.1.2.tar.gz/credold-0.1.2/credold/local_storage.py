import json
from pathlib import Path

from credold.storage import Storage


class LocalStorage(Storage):
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def save(self, data: dict) -> None:
        # 中間ディレクトリがない場合は作成する
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open(mode="w") as f:
            json.dump(data, f, indent=4)

    def load(self) -> dict:
        if not self.file_path.exists():
            msg = f"{self.file_path} is not found."
            raise FileNotFoundError(msg)

        with self.file_path.open() as f:
            return json.load(f)
