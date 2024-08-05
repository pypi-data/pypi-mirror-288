from pathlib import Path
from unittest import TestCase

from credold.local_storage import LocalStorage

DUMMY_DATA = {"token": "dummy"}


class TestLocalStorage(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_指定したファイルがないときは例外を投げる(self):
        # Then: 例外が投げられることを確認する
        with self.assertRaises(FileNotFoundError):
            # When: ファイルがない場合
            suite = LocalStorage(file_path="not_found")
            suite.load()

    def test_指定したファイルがないときは新規作成する(self):
        # Given
        file_path = "/tmp/test_local_storage.json"
        # テストのため、もし既にファイルがある場合は削除する
        Path(file_path).unlink(missing_ok=True)

        suite = LocalStorage(file_path=file_path)
        suite.save(data=DUMMY_DATA)
        # Then: ファイルが作成される
        self.assertEqual(suite.load(), DUMMY_DATA)

    def test_中間ディレクトリがないときは新規作成する(self):
        # Given
        dir = "/tmp/test_local_storage"
        file_path = "/tmp/test_local_storage/test_local_storage.json"
        # テストのため、既にファイル・フォルダがある場合は削除する
        Path(file_path).unlink(missing_ok=True)
        try:
            Path(dir).rmdir()
        except FileNotFoundError:
            pass

        suite = LocalStorage(file_path=file_path)
        suite.save(data=DUMMY_DATA)

        # Then: ファイルが作成される
        self.assertEqual(suite.load(), DUMMY_DATA)

    def test_既にファイルがあるときは上書きする(self):
        # Given
        file_path = "/tmp/test_local_storage.json"
        # テストのため、もし既にファイルがある場合は削除する
        Path(file_path).unlink(missing_ok=True)

        suite = LocalStorage(file_path=file_path)
        suite.save(data=DUMMY_DATA)
        # When: 既にファイルがある場合
        suite.save(data={"token": "new_dummy"})

        # Then: ファイルが上書きされる
        self.assertEqual(suite.load(), {"token": "new_dummy"})
