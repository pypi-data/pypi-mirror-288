#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 上午10:43
# @File    : openai.py
# @desc    : openai api


from typing import Optional
from raglink.llms.base import LLMBase
from raglink.utils.logger import logger
from langchain_openai.chat_models import ChatOpenAI


class OpenAILLM(LLMBase):
    def __init__(
        self,
        api_key,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None

    ):
        self.api_key = api_key
        self.base_url = base_url

        self.model = "gpt-4o" if model is None else model
        self.temperature = 0 if temperature is None else temperature
        self.max_tokens = 1000 if max_tokens is None else max_tokens

    def gen(self):
        chat = ChatOpenAI(
            openai_api_key=self.api_key,
            base_url=self.base_url,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        logger.debug(f"初始化 OpenAi 模型: {self.model}, temperature: {self.temperature}, max_tokens: {self.max_tokens}")
        return chat


