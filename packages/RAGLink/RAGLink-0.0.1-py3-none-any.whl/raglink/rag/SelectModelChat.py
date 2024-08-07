#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/6/23 16:03
# @Author : justin.郑 3907721@qq.com
# @File : SelectModelChat.py
# @desc : 选择对话模型

import os
from dotenv import load_dotenv
load_dotenv()

from raglink.utils.config import config
from raglink.utils.logger import logger

from langchain_community.chat_models import MiniMaxChat
from langchain_openai.chat_models import ChatOpenAI


class SelectModelChat:
    def __init__(self):
        self.chat_model_config = config.get_chat_model_config()

    def get(self):
        """
        获取对话模型
        :return:
        """

        if self.chat_model_config['chat_name'] == "minimax":
            chat = MiniMaxChat(
                minimax_group_id=os.getenv("MINIMAX_GROUP_ID"),
                minimax_api_key=os.getenv("MINIMAX_API_KEY"),
                model=self.chat_model_config['model_name'],
                temperature=self.chat_model_config['temperature']
            )
        if self.chat_model_config['chat_name'] == "openai":
            chat = ChatOpenAI(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                model=self.chat_model_config['model_name'],
                temperature=self.chat_model_config['temperature']
            )
        if self.chat_model_config['chat_name'] == "deepseek":
            chat = ChatOpenAI(
                openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
                openai_api_base=os.getenv('DEEPSEEK_API_BASE'),
                model=self.chat_model_config['model_name'],
                temperature=self.chat_model_config['temperature']
            )
        logger.info(f"SelectModelChat 使用 {self.chat_model_config['model_name']} 模型， temperature: {self.chat_model_config['temperature']}")
        return chat