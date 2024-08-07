#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/3 15:17
# @Author : justin.郑 3907721@qq.com
# @File : base.py
# @desc : LLMs 基类


from typing import Optional
from abc import ABC, abstractmethod


class LLMBase(ABC):
    @abstractmethod
    def gen(self, messages):
        """
        根据给定的消息生成响应
        :param messages: List of message dicts containing 'role' and 'content'
        :return: 生成的响应
        """
        pass
