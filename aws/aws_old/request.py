#!/usr/bin/env python3

from re import search
from time import time
from os.path import join
from requests import post
from requests.exceptions import JSONDecodeError


class LambdaRequest:
    def __init__(self, token) -> None:
        self.timeout = 60
        self.__headers = {}
        self.__last_request = 0
        self.base_url = ""
        self.token = token

    def request(self, method: str, url: str, body={}) -> dict:
        if self.__last_request + 30 * 60 <= time():
            self.login()
        response = self.__request(method, url, body)
        self.__last_request = time()
        return response

    def login(self) -> None:
        """ログインAPIを実行"""
        self.__request("GET", "/login")
        try:
            body = {
                "email": self.__credentials.email,
                "password": self.__credentials.password,
            }
            self.__request("POST", "/login", body)
        except Exception as e:
            raise e

    def __request(self, method: str, url: str, body={}) -> dict:
        url = url[1:] if url and url[0] == "/" else url
        query = {
            "url": join(self.base_url, url),
            "headers": self.__headers,
            "timeout": self.timeout,
        }
        body["_token"] = self.token
        body["_api"] = url
        body["_method"] = method
        res = post(**query, json=body)

        if res.status_code != 200:
            try:
                text = str(res.json())
            except JSONDecodeError:
                raise TypeError(f"APIが実行できませんでした。{res.status_code}")
            raise TypeError(f"{text}: {res.status_code}")

        if "Set-Cookie" in res.headers:
            cookie = res.headers["Set-Cookie"]
            self.__headers = {
                "Cookie": cookie,
                "X-CSRF-TOKEN": search("(?<=csrf_access_token=)[^;]*", cookie)[0],
                "Content-Type": "application/json",
                "X-API-KEY": self.__credentials.api_key,
            }
        return res.json()
