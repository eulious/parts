#!/usr/bin/env python3

"""
# 設定
app = LambdaURL()
auth = Authorization(app, TOKEN_PASSWORD, SESSION_PASSWORD)
id = auth.require_session()
"""

from re import search
from json import loads, dumps
from time import time
from base64 import b64decode, b64encode
from hashlib import sha256
from traceback import format_exc
from .lambda_url import LambdaURL
from .bottle_router import HTTPError


class Authentication:
    def __init__(
        self, app: LambdaURL, token_password: str, session_password: str
    ) -> None:
        self.__session_password = session_password
        self.__token_password = token_password
        self.app = app

    def issue_session(self, id: str):
        token = self.__encode({"id": id}, self.__session_password)
        self.app.set_cookie(
            f"token={token}; max-age=315360000; SameSite=None; Secure; HttpOnly"
        )

    def require_session(self):
        try:
            for cookie in self.app.cookies:
                m = search("(?<=^token\=)[^;]+(?=(;|$))", cookie)
                if m:
                    token = m.group()
            payload = self.__decode(token, self.__session_password)
            assert "id" in payload
        except Exception as e:
            print(format_exc())
            raise HTTPError(401, f"無効なセッションです: {format_exc()}")
        return payload["id"]

    def issue_token(self, id: str):
        payload = {"id": id, "iat": int(time())}
        return self.__encode(payload, self.__token_password)

    def require_token(self):
        try:
            token = self.app.headers["token"]
            payload = self.__decode(token, self.__token_password)
            assert "id" in payload
            assert time() < payload["iat"] + 30 * 60
        except Exception as e:
            print(format_exc())
            raise HTTPError(401, f"無効なトークンです: {format_exc()}")
        return payload["id"]

    def __hash(self, text: str):
        digest = sha256(text.encode()).digest()
        return b64encode(digest).decode().replace("=", "-")

    def __encode(self, d: dict, passwd: str):
        b64 = b64encode(dumps(d).encode()).decode()
        b64 = b64.replace("=", "-")
        return b64 + "." + self.__hash(b64 + passwd)

    def __decode(self, token: str, passwd: str):
        [b64, hash] = token.split(".")
        assert hash == self.__hash(b64 + passwd)
        return loads(b64decode(b64.replace("-", "=")).decode())
