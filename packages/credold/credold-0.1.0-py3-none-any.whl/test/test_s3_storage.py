from unittest import TestCase

from credold.s3_storage import S3Storage

DUMMY_DATA = {"token": "dummy"}


class TestS3Storage(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_指定したファイルがS3ないときは例外を投げる(self):
        # Then: 例外が投げられることを確認する
        with self.assertRaises(FileNotFoundError):
            # When: ファイルがない場合
            suite = S3Storage.localstack(bucket_name="dummy", key="not_found.json")
            suite.load()

    def test_S3に保存できる(self):
        # Given
        suite = S3Storage.localstack(bucket_name="credold-sample")

        # When
        suite.save(data=DUMMY_DATA)

        # Then
        actual = suite.load()
        self.assertEqual(actual, DUMMY_DATA)
