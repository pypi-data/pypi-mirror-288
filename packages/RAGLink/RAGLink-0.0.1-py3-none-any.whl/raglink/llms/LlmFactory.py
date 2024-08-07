#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 上午10:16
# @File    : LlmFactory.py
# @desc    : LLM工厂类


from raglink.utils.tools import load_class


# LLM提供者名称到类名的映射
provider_to_class = {
    "openai": "raglink.llms.openai.OpenAILLM",
    "minimax": "raglink.llms.minimax.MinimaxLLM",
    "deepseek": "raglink.llms.deepseek.DeepSeekLLM"
}


class LlmFactory:
    def create(provider_name, config):
        class_type = provider_to_class.get(provider_name)
        if class_type:
            llm_instance = load_class(class_type)
            # base_config = BaseLlmConfig(**config)
            return llm_instance(**config)
        else:
            raise ValueError(f"Unsupported Llm provider: {provider_name}")

