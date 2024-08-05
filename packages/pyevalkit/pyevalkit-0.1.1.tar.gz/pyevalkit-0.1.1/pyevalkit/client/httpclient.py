#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/10 16:56
import json
import re
from io import StringIO

import requests
from loguru import logger
from requests import exceptions

from pyevalkit.client.media import ContentTypes
from pyevalkit.comm import cache
from pyevalkit.comm.jsonpath import JsonHandle
from pyevalkit.comm.validator import Assert


def post(url, method="POST", payload=None, **kwargs):
    return request(url=url, method=method, payload=payload, **kwargs).execute()


def get(url, method="GET", payload=None, **kwargs):
    return request(url=url, method=method, payload=payload, **kwargs).execute()


def request(url, method, payload=None, **kwargs):
    return HTTPRequest(url=url, method=method, payload=payload, **kwargs)


class HTTPRequest(object):

    def __init__(self, url, method, payload=None, **kwargs):
        self.url = url
        self.method = method
        self.payload = payload
        self.kwagrs = kwargs

    def execute(self):
        try:
            headers = self.kwagrs.get("headers")
            if headers is None:
                response = requests.request(url=self.url, method=self.method, params=self.payload, **self.kwagrs)
            else:
                content_type = headers.get("Content-Type")
                if content_type is None:
                    response = requests.request(url=self.url, method=self.method, params=self.payload, **self.kwagrs)
                elif content_type in ContentTypes.APPLICATION_JSON:
                    response = requests.request(url=self.url, method=self.method, json=self.payload, **self.kwagrs)
                elif content_type == ContentTypes.APPLICATION_FORM_URLENCODED:
                    response = requests.request(url=self.url, method=self.method, data=self.payload, **self.kwagrs)
                elif content_type in ContentTypes.MULTIPART_FORM_DATA:
                    for key, value in self.kwagrs.items():
                        if key == "headers":
                            del self.kwagrs[key]["Content-Type"]
                        if key == "payload":
                            del self.kwagrs[key]["files"]

                    response = requests.request(url=self.url, method=self.method, data=self.payload, **self.kwagrs)
                else:
                    raise TypeError(f"暂不支持 {content_type} 类型！")
        except exceptions.RequestException as e:
            raise exceptions.RequestException(f"请求失败，异常信息：{e}")
        except Exception as e:
            raise Exception(f"请求失败，未知错误：{e}")

        return HTTPResponse(response=response)


class ResponseHandle:

    def __init__(self, response):
        self._response = HTTPResponse(response)

    def verify(self, items):
        for check in items:
            if not isinstance(check, dict):
                raise ValueError(f"断言项必须是字典类型！")

            for key, value in check.items():
                if not isinstance(value, list):
                    raise ValueError(f"断言参数必须是列表类型！")

                item = value[0]
                if len(value) == 2:
                    expect = value[1]
                    if item.lower() == "status":
                        actual = self._response.status_code
                        Assert.check(key, actual, expect)

                elif len(value) == 3:
                    expr = value[1]  # 表达式
                    expect = value[2]  # 预期值
                    if item.lower() == "content":
                        actual = self._response.content.read(expr)
                        Assert.check(key, actual, expect)
                    elif item.lower() == "headers":
                        actual = self._response.headers.read(expr)
                        Assert.check(key, actual, expect)
                    else:
                        raise ValueError(f" {item} 暂不支持断言!")

                else:
                    raise ValueError(f" 断言参数列表长度错误！")

    def add_cache(self, items):
        for extract in items:
            if not isinstance(extract, dict):
                raise ValueError(f"提取项必须是字典类型！")

            for key, value in extract.items():
                if not isinstance(value, list):
                    raise ValueError(f"提取参数必须是列表类型！")

                name = value[0]  # 缓存名
                expr = value[1]  # 表达式
                if key.lower() == "cookies":
                    cache.set(name, self._response.cookies.read(expr))
                elif key.lower() == "content":
                    cache.set(name, self._response.content.read(expr))
                else:
                    raise ValueError(f" {key} 暂不支持提取！")


class HTTPResponse(object):

    def __init__(self, response):
        self._response = response

    @property
    def inst(self):
        return self._response

    def to_dict(self, *args, **kwargs):
        return self._response.json(*args, **kwargs)

    def to_text(self, **kwargs):
        return json.dumps(self._response.json(), ensure_ascii=False, **kwargs)
        # content_type = self._response.headers.get("content-type")
        # if content_type:
        #     if content_type in ContentTypes.APPLICATION_JSON:
        #         return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)
        #     else:
        #         return None
        # return None

    def raise_for_status(self):
        return self._response.raise_for_status()

    def iter_lines(self):
        return self._response.iter_lines()

    @property
    def text(self):
        return self._response.text

    @property
    def byte(self):
        return self._response.content

    @property
    def content(self):
        content = self._response.json()
        return JsonHandle(obj=content)

    @property
    def cookies(self):
        cookies = self._response.cookies.get_dict()
        return JsonHandle(obj=cookies)

    @property
    def headers(self):
        headers = self._response.headers
        return JsonHandle(obj=dict(headers))

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def elapsed(self):
        return self._response.elapsed.total_seconds()

    @property
    def request(self):
        class Request(object):
            def __init__(self, response):
                self._request = response.request

            @property
            def url(self):
                return self._request.url

            @property
            def method(self):
                return self._request.method

            @property
            def headers(self):
                return self._request.headers

            @property
            def payload(self):
                return self._request.body

            def to_dict(self):
                items = dict()
                items["url"] = self.url
                items["method"] = self.method

                content_type = self.headers.get("Content-Type")
                if content_type:
                    if content_type in ContentTypes.APPLICATION_JSON:
                        body = self._request.body
                        if body:
                            items["payload"] = json.loads(body.decode(encoding="utf-8"))
                        else:
                            items["payload"] = None
                    else:
                        items["payload"] = None

                items["headers"] = dict(self.headers)
                return items

            def to_text(self, indent=None):
                return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

        return Request(response=self._response)

    def event_stream(self):
        output = StringIO()
        for line in self._response.iter_lines():
            if line:
                text = line.decode("utf-8")
                match = re.search(r"data: (.*)", text)
                if match:
                    output.write(text.group(1))
        return output.getvalue()

    @property
    def action(self):
        return ResponseHandle(self._response)

# def response_cehck(resp, items):
#     return ResponseHandle(resp).check(items)
#
#
# def response_cache(resp, items):
#     return ResponseHandle(resp).extract(items)
#
#
# def response(resp):
#     return ResponseHandle(resp)


class ResponseContentType:

    def __init__(self, response):
        self._response = HTTPResponse(response)

    def __call__(self, resp):
        pass

    @property
    def _headers(self):
        return self._response.headers

    def body(self):
        content_type = self._headers.read("content-type")
        if content_type:
            return self._response.text

        if "event-stream" in content_type:
            res = self._response.event_stream()
        elif "application/json" in content_type:
            res = self._response.to_text()
        elif "application/octet-stream" in content_type:
            with open("", "w", encoding="utf-8") as file:
                file.write(self._response.byte)
            res = ""
        elif "image/" in content_type:
            with open("", "w", encoding="utf-8") as file:
                file.write(self._response.byte)
            res = ""




