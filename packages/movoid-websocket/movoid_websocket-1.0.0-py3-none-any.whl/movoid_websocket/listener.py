#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : listener
# Author        : Sun YiFan-Movoid
# Time          : 2024/8/3 15:09
# Description   : 
"""
import threading
import time
from typing import Dict

import websocket


class OneListener:
    def __init__(self, url: str):
        self._url = url
        self._ws = websocket.WebSocket()
        self._thread = threading.Thread()
        self._history = []
        self._stop = False
        self._sign = {}
        self.start()

    def _thread_listen(self):
        if not self._ws.connected:
            self._ws.connect(self._url)
        while self._ws.connected and not self._stop:
            try:
                receive_text = self._ws.recv()
                time_now = time.time()
                self._history.append([time_now, receive_text])
            except Exception:
                self._ws.close()
                self._ws.connect(self._url)

    def sign(self, sign_name="__default__"):
        sign_name = str(sign_name)
        self._sign[sign_name] = time.time()
        self.start()

    def start(self):
        if not self._thread.is_alive():
            self._thread = threading.Thread(target=self._thread_listen)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        self._stop = False

    def _find_history_text_after_sign(self, sign=None):
        """
        获取从sign之后的所有获得信息
        :param sign: 不填就全部返回
        :return:
        """
        if sign is None or sign not in self._sign:
            re_list = [_ for _ in self._history]
        else:
            re_list = [_ for _ in self._history if _[0] >= self._sign[sign]]
        return re_list

    def wait_until_check_pass(self, check_function, sign=None, return_time=False, timeout=5):
        """
        最多等待一定时间后，检查是否存在某段文本满足要求，总是会寻找最新的文本
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param return_time: 返回时是否返回时间
        :param timeout: 最大的等待时间
        :return: 时间+文本，如果没有就返回None
        """
        if callable(check_function):
            real_check_function = check_function
        else:
            def real_check_function(check_text: object) -> bool:
                return str(check_text) == str(check_function)
        text_list = self._find_history_text_after_sign(sign)
        for text_one in text_list[::-1]:
            if real_check_function(text_one[1]):
                pass_text = text_one
                break
        else:
            start_time = time.time()
            last_time = 0
            text_check = len(text_list)
            while last_time < timeout:
                loop_start_time = time.time()
                now_text_list = self._find_history_text_after_sign(sign)
                while text_check < len(now_text_list):
                    text_one = now_text_list[text_check]
                    if real_check_function(text_one[1]):
                        pass_text = text_one
                        break
                    else:
                        text_check += 1
                else:
                    loop_last_time = time.time() - loop_start_time
                    time.sleep(max(0.2 - loop_last_time, 0))
                    last_time = time.time() - start_time
                    continue
                break
            else:
                pass_text = [0, None]
        if return_time:
            return pass_text
        else:
            return pass_text[1]


class WebSocketListener:
    def __init__(self):
        self._ws: Dict[str, OneListener] = {}

    @property
    def ws(self):
        return self._ws

    def start(self, url, name=None):
        name = str(url) if name is None else str(name)
        self._ws[name] = OneListener(url)

    def sign(self, name, sign):
        self._ws[name].sign(sign)

    def wait_until_check_pass(self, name, check_function, sign=None, return_time=False, timeout=5):
        """
        最多等待一定时间后，检查是否存在某段文本满足要求，总是会寻找最新的文本
        :param name: 标签名，一定要输入
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param return_time: 返回时是否返回时间
        :param timeout: 最大的等待时间
        :return: 时间+文本，如果没有就返回None
        """
        return self._ws[name].wait_until_check_pass(check_function=check_function, sign=sign, return_time=return_time, timeout=timeout)

    def stop(self, name):
        self._ws[name].stop()

    def delete(self, name):
        if name in self._ws:
            self.stop(name)
            self._ws.pop(name)
