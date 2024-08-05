#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/8/2 21:56


import websocket
from threading import Thread
import time

import websockets
from loguru import logger
from websockets import ConnectionClosed


class WebSocketClient:

    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        self.websocket = await websockets.connect(url)
        logger.info(f"已连接到WebSocket服务器: {url}")

    async def receive_message(self, max_recvs):
        messages = []
        try:
            message_count = 0
            while message_count < max_recvs:
                message = await self.websocket.recv()
                logger.info(f"接收WebSocket消息: {message}")
                messages.append(message)
                message_count += 1
            return messages
        except ConnectionClosed:
            logger.error(f"连接被关闭，无法接收消息。")
        except Exception as e:
            logger.error(f"接收消息时出现异常：{e}")

    async def send_message(self, message):
        try:
            await self.websocket.send(message)
            logger.info(f"发送WebSocket消息: {message}")
        except ConnectionClosed:
            logger.error("连接被关闭，无法发送消息。")
        except Exception as e:
            logger.error(f"发送消息时出现异常：{e}")

    async def close_connection(self):
        try:
            await self.websocket.close()
            logger.info("已主动关闭WebSocket连接。")
        except Exception as e:
            logger.error(f"关闭WebSocket连接时发生错误: {e}")
