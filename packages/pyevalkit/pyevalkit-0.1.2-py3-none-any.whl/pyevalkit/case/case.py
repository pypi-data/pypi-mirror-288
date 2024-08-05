#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/10 19:06
import json
import re
from pathlib import Path
from urllib.parse import urlencode

import allure
import pytest
from loguru import logger

from pyevalkit.client import httpclient
from pyevalkit.client.encoder import encode_files
from pyevalkit.comm import template, cache
from pyevalkit.comm.jsonpath import JsonHandle
from pyevalkit.comm.validator import Assert


class _Request(JsonHandle):
    def __init__(self, obj: dict):
        super().__init__(obj=obj)

    @property
    def url(self) -> str:
        return self.get(expr="$.url")

    @property
    def ws_uri(self):
        payload = self.payload.values()
        return f"{self.url}?{urlencode(payload)}"

    @property
    def method(self) -> str:
        return self.get(expr="$.method")

    @property
    def headers(self):
        rest = self.get(expr="$.headers")
        return JsonHandle(obj=rest)

    @property
    def cookies(self):
        rest = self.get(expr="$.cookies")
        return JsonHandle(obj=rest)

    @property
    def payload(self):
        payload = self._obj.get("payload")
        return JsonHandle(obj=payload)

    @property
    def files(self):
        files = self.payload.read("files")
        return files

    @property
    def message(self):
        message = self._obj.get("message")
        return JsonHandle(obj=message)


class Case(JsonHandle):

    def __init__(self, case):
        super().__init__(obj=case)

    @property
    def cid(self):
        return self.get(expr="$.id")

    @property
    def skip(self):
        return self.get(expr="$.skip")

    @property
    def epic(self):
        return self.get(expr="$.epic")

    @property
    def feature(self):
        return self.get(expr="$.feature")

    @property
    def story(self):
        return self.get(expr="$.story")

    @property
    def title(self):
        return self.get(expr="$.title")

    @property
    def level(self):
        return self.get(expr="$.level")

    @property
    def verify(self):
        return self.get(expr="$.validate")

    @property
    def extract(self):
        return self.get(expr="$.extract")

    @property
    def request(self):
        request = self._obj.get("request")
        return _Request(obj=request)

    def execute(self):
        request = self.request.to_text()
        if self.skip:
            pytest.skip(reason=f"用例 {self.cid} 已被标记为不执行！")

        else:
            url = self.request.url
            method = self.request.method
            headers = self.request.headers.values()
            payload = self.request.payload.values()

            allure.attach("请求参数", request, allure.attachment_type.JSON)
            logger.info(f"发送请求 >>>>> {self.title} | {method.center(4)} | {request}")

            if payload:
                for key, value in payload.items():
                    if key == "files":
                        payload[key] = encode_files(value)
                        break

            try:
                files = payload.get("files")
                client = httpclient.request(url, method, payload, files=files, headers=headers)
                response = client.execute()
            except Exception as e:
                raise e

            status_code = str(response.status_code)
            if not status_code.startswith("2"):
                logger.error(f"接收响应 <<<<< {self.title} | {status_code.center(4)} | {response.text}")
                return response

            else:
                file_path = Path.cwd() / "files/download"
                content_type = headers.get("Content-Type")
                # 响应参数添加到附件中
                if content_type is None:
                    attach_body = response.text
                    attach_type = allure.attachment_type.TEXT

                elif "event-stream" in content_type:
                    attach_body = response.event_stream()
                    attach_type = allure.attachment_type.TEXT

                elif "application/json" in content_type:
                    attach_body = response.content.to_text()
                    attach_type = allure.attachment_type.JSON

                elif "application/octet-stream" in content_type:
                    attach_body = "未处理的下载文件"
                    attach_type = allure.attachment_type.TEXT

                else:
                    attach_body = response.content.to_text()
                    attach_type = allure.attachment_type.TEXT

                allure.attach("响应参数", attach_body, attach_type)
                logger.info(f"接收响应 <<<<< {self.title} | {status_code.center(4)} | {attach_body}")
                # logger.info(f"接收响应 <<<<< {self.title} | {status_code.center(4)} | {response.inst.raw()}")

                # 添加allure属性
                allure.dynamic.epic(self.epic)
                allure.dynamic.story(self.story)
                allure.dynamic.title(self.title)
                allure.dynamic.feature(self.feature)

                if self.verify:
                    response.action.verify(self.verify)

                if self.extract:
                    response.action.add_cache(self.extract)

        return response

    def build(self, url=None, method=None, *args, **kwargs):
        if url is not None:
            url = self.request.url

        if method is not None:
            method = self.request.method

        return httpclient.request(url=url, method=method, *args, **kwargs)

    def __str__(self):
        return json.dumps(self._obj, ensure_ascii=False)


class Render(Case):

    def __init__(self, obj: dict):
        self._globals = obj.get("globals")
        self._testcase = obj.get("testcase")
        super().__init__(case=self._testcase)

    def render(self):
        # 更新模板函数
        context = dict()
        context.update(template.builtin)

        # 渲染全局节点
        output = template.render(self._globals, **context)

        # 更新模板函数
        context.update(output)

        # 渲染用例节点
        output = template.render(self._testcase, **context)
        return Case(case=output)


