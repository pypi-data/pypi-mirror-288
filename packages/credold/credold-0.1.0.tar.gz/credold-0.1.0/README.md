## localstack

locakstackを利用することで、AWSのリソースをローカルで扱うことができる。

### 利用のための準備

`~/.aws/credentials`に、以下のようなアカウントを作成

```
[localstack]
aws_access_key_id = dummy
aws_secret_access_key = dummy
region=ap-northeast-1
```

### 利用例

```shell
aws --endpoint-url=http://localhost:4567 --profile localstack {awsコマンド}
```

たとえばS3バケットを作成した場合は、以下のようなコマンドを実行する。

```shell
# バケット作成
aws --endpoint-url=http://localhost:4567 --profile localstack s3 mb s3://credold-sample

# バケット一覧表示
aws --endpoint-url=http://localhost:4567 --profile localstack s3 ls
```

## PyPi

```shell
python setup.py sdist bdist_wheel
```
