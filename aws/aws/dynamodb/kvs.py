#!/usr/bin/env python3

"""
DynamoDBで以下の形式でテーブルを作成する
- パーティションキー: key
- キャパシティーモード: オンデマンド
"""

from json import dumps, loads
from boto3 import resource
from typing import Any, Dict
from json.decoder import JSONDecodeError


class KVS:
    def __init__(self, tablename="kvs"):
        self.db = resource("dynamodb").Table(tablename)

    def put(self, key: str, value: Any):
        return self.db.put_item(Item={"key": key, "value": dumps(value)})

    def get(self, key: str) -> Any:
        res = self.db.get_item(Key={"key": key})
        if "Item" in res:
            return self.__parse(res["Item"]["value"])
        else:
            return None

    def delete(self, key: str):
        return self.db.delete_item(Key={"key": key})

    def scan(self) -> Dict[str, Any]:
        res = self.db.scan()
        if "Items" not in res:
            return {}
        data = res["Items"]
        while "LastEvaluatedKey" in res:
            res = self.db.scan(ExclusiveStartKey=res["LastEvaluatedKey"])
            data.extend(res["Items"])
        return {item["key"]: self.__parse(item["value"]) for item in data}

    def __parse(self, value):
        try:
            return loads(value)
        except JSONDecodeError:
            return value
