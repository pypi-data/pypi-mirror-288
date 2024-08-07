#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/6/23 15:55
# @Author : justin.郑 3907721@qq.com
# @File : SelectEmbeddings.py
# @desc : 选择Embeddings向量化

# BCEmbedding  https://huggingface.co/maidalun1020/bce-embedding-base_v1
# pip install BCEmbedding

import os
from dotenv import load_dotenv
from raglink.utils.config import config
# from BCEmbedding import RerankerModel
# from BCEmbedding import EmbeddingModel

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import MiniMaxEmbeddings

load_dotenv()


class SelectEmbeddings:
    def __init__(self):
        self.embeddings_config = config.get_embeddings_config()

    # 获取Embeddings model
    def get_embeddings(self):
        """
        获取 Embeddings
        :return:
        """
        if self.embeddings_config['embeddings_model_name'] == "minimax":
            embeddings = MiniMaxEmbeddings(
                minimax_group_id=os.getenv("MINIMAX_GROUP_ID"),
                minimax_api_key=os.getenv("MINIMAX_API_KEY")
            )
        if self.embeddings_config['embeddings_model_name'] == "openai":
            embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        if self.embeddings_config['embeddings_model_name'] == "BCEmbedding":
            # ===================================================================
            # 使用 BCEmbedding 设置本地模型
            from BCEmbedding import EmbeddingModel
            embeddings = EmbeddingModel(
                model_name_or_path="models/bce-embedding-base_v1"
            )

            # ===================================================================
            # 使用 HuggingFaceEmbeddings 方式
            # os.environ['CURL_CA_BUNDLE'] = ''
            # os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
            # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"
            #
            # model_name = 'maidalun1020/bce-embedding-base_v1'
            # model_kwargs = {'device': 'cuda'}
            # encode_kwargs = {'batch_size': 64, 'normalize_embeddings': True}
            #
            # embeddings = HuggingFaceEmbeddings(
            #     model_name=model_name,
            #     model_kwargs=model_kwargs,
            #     encode_kwargs=encode_kwargs
            # )

        return embeddings

    # 获取Reranker model
    def get_reranker(self):
        if self.embeddings_config['reranker_model_name'] == "BCEmbedding":
            # 使用 BCEmbedding 方式
            from BCEmbedding import RerankerModel
            reranker = RerankerModel(
                model_name_or_path="models/bce-reranker-base_v1"
            )
        return reranker

