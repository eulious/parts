#!/usr/bin/env python3

"""
# 設定
app = LambdaURL()

def lambda_handler(event, _):
    return app.request(event)

@app.post("/test/<id:int>")
def test()
    return {"status": "ok"}

"""

from json import dumps, loads
from base64 import b64decode
from traceback import format_exc
from .bottle_router import HTTPError, Router


class LambdaURL:
    def __init__(self):
        self.cookies = []
        self.headers = {}
        self.querys = {}
        self.__router = Router()
        self.__set_cookies = []
        self.domain = ""
        self.method = ""
        self.path = ""

    def get(self, url: str):
        return self.__add(url, "GET")

    def post(self, url: str):
        return self.__add(url, "POST")

    def put(self, url: str):
        return self.__add(url, "PUT")

    def delete(self, url: str):
        return self.__add(url, "DELETE")

    def __add(self, url: str, method: str):
        def _wrapper(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.__router.add(url, method, func)
            return wrapper

        return _wrapper

    def request(self, event):
        try:
            func = self.__parse(event)
            return self.__response(200, func())
        except HTTPError as e:
            return self.__response(e.status, e.body)
        except:
            print(format_exc())
            return self.__response(500, {"status": "ng", "detail": format_exc()})
            return self.__response(
                500, {"status": "ng", "detail": "internal server error"}
            )

    def __parse(self, event):
        self.__set_cookies = []
        self.cookies = event["cookies"] if "cookies" in event else []
        self.headers = event["headers"]
        self.query_params = (
            event["queryStringParameters"] if "queryStringParameters" in event else {}
        )
        self.domain = event["requestContext"]["domainName"]
        self.method = event["requestContext"]["http"]["method"]
        self.path = event["requestContext"]["http"]["path"]
        try:
            self.body = loads(b64decode(event["body"].encode()).decode())
        except:
            self.body = {}
        func, path_params = self.__router.match(
            {"REQUEST_METHOD": self.method, "PATH_INFO": self.path}
        )
        self.path_params = path_params
        return func

    def set_cookie(self, cookie: str):
        self.__set_cookies.append(cookie)

    def __response(self, status_code: int, body={"status": "ok"}):
        response = {
            "statusCode": status_code,
            "body": dumps(
                body,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            "isBase64Encoded": False,
        }
        if len(self.__set_cookies):
            response["cookies"] = self.__set_cookies
        return response
