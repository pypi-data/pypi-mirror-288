#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 下午4:56
# @File    : minimax.py
# @desc    : MiniMax API


from typing import Optional
from raglink.utils.logger import logger
from raglink.llms.base import LLMBase
from langchain_community.chat_models import MiniMaxChat


class MinimaxLLM(LLMBase):
    def __init__(
        self,
        api_key,
        group_id,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None

    ):
        self.api_key = api_key
        self.group_id = group_id
        self.model = "abab6.5s-chat" if model is None else model
        self.temperature = 0 if temperature is None else temperature
        self.max_tokens = 8192 if max_tokens is None else max_tokens

    def gen(self):
        chat = MiniMaxChat(
            minimax_api_key=self.api_key,
            minimax_group_id=self.group_id,
            model=self.model,
            temperature=self.temperature,
            tokens_to_generate=self.max_tokens
        )
        logger.debug(f"初始化 Minimax 模型: {self.model}, temperature: {self.temperature}, max_tokens: {self.max_tokens}")
        return chat