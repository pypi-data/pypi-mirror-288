#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/7/30 15:56


# import websocket
#

import asyncio
import json
from datetime import datetime
from urllib.parse import urlencode

import websockets

import asyncio
import websockets

from pyevalkit.comm import mock


class WebSocketClient:

    def __init__(self, uri):
        self.uri = uri
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        print("已连接到 WebSocket 服务器:", self.uri)

    async def receive_messages(self, max_recvs):
        received_messages = []
        try:
            message_count = 0
            while message_count < max_recvs:
                # await asyncio.sleep(1)
                message = await self.connection.recv()
                print(f"第{message_count}次：", message)
                received_messages.append(json.loads(message))

                message_count += 1
        except websockets.exceptions.ConnectionClosed:
            print("连接被服务器关闭。")
        except Exception as e:
            print(f"发生错误: {e}")
        return received_messages

    async def send_message(self, message):
        try:
            await self.connection.send(message)
            print("发送消息到服务器:", message)
        except websockets.exceptions.ConnectionClosed:
            print("1连接关闭，无法发送消息。")
        except Exception as e:
            print(f"发送消息时发生错误: {e}")

    async def close_connection(self):
        try:
            await self.connection.close()
            print("WebSocket 连接已关闭。")
        except Exception as e:
            print(f"关闭连接时发生错误: {e}")


async def main():
    token = "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiIzZmM1ODEzMS0wMjg5LTRmOWMtOWUyOS01M2VkNWQ1ODA0NTciLCJpc3MiOiJodHRwczovL3d3dy55dW50b25neHVuLmNvbS8iLCJzdWIiOiIyMDAiLCJhdWQiOiJhaWhlbHBlciIsImlhdCI6MTcyMjc0ODc1Nn0.0zXfNFOK-uckrsfKCBjZ36UItVYvG_6UrGftA03XzqkfzAKwE0k_crgBZxqIAB_msLWlHzWzS00JjBevzVJc6g"
    uuid = mock.uuid().replace("-", "")
    # uuid = "f2e6ab11f9354129b64344fc49f419d3"
    data = {
        "callId": f"text_test{uuid}",
        "sceneId": 36,
        "associateData": {"age": "12", "custom2": "def"},
        "wsurl": "wss://copilot.yuntongxun.com/aihelper-websocket",
        "token": token
    }

    uri = "wss://copilot.yuntongxun.com/aihelper-websocket?callId=text_test1e95f1eec89c490a9e4beb325d946696&sceneId=35&associateData={%22age%22:%2212%22,%22custom2%22:%22def%22}&wsurl=wss://copilot.yuntongxun.com/aihelper-websocket&token=eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiIzZmM1ODEzMS0wMjg5LTRmOWMtOWUyOS01M2VkNWQ1ODA0NTciLCJpc3MiOiJodHRwczovL3d3dy55dW50b25neHVuLmNvbS8iLCJzdWIiOiIyMDAiLCJhdWQiOiJhaWhlbHBlciIsImlhdCI6MTcyMjc0ODc1Nn0.0zXfNFOK-uckrsfKCBjZ36UItVYvG_6UrGftA03XzqkfzAKwE0k_crgBZxqIAB_msLWlHzWzS00JjBevzVJc6g"
    client = WebSocketClient(uri)

    # 1. 建立连接
    await client.connect()

    # 2. 创建接收消息的任务
    receive_task = asyncio.create_task(client.receive_messages())

    # message = {
    #     "role": 1,
    #     "callId": f"text_test{uuid}",
    #     "messageId": "73d2b860-aa8b-46f0-b66b-9e8bc710392e",
    #     "type": 1,
    #     "content": "我今年40岁",
    #     "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "createTimeMillis": int(datetime.now().timestamp() * 1000),
    # }

    # await receive_task

    # 3. 不断等待输入并发送消息
    # while True:
    message = {"role": 1, "callId": "text_test1e95f1eec89c490a9e4beb325d946696",
               "messageId": "741c8598-7424-4127-a43c-43e4557f61c1", "type": 1, "content": "我今年40岁",
               "createTime": "2024-08-04 14:00:17", "createTimeMillis": 1722751217426}

    await client.send_message(json.dumps(message, ensure_ascii=False))
    # await asyncio.sleep(1)  # 暂停一秒以避免过于频繁的发送

    await asyncio.sleep(3)
    receive_task.cancel()

    # 4. 关闭连接
    await client.close_connection()

# 运行主函数
# asyncio.run(main())
