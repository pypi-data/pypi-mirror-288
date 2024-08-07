#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/7/30 下午12:22
# @File    : QdrantDatabase.py
# @desc    : Qdrant数据库基类


import os
from dotenv import load_dotenv
from raglink.utils.logger import logger
from qdrant_client import QdrantClient

load_dotenv()


class QdrantDatabase:
    def __init__(self, collection_name, is_local=True):
        """
        初始化
        :param collection_name:     集合名称
        :param is_local:            是否本地化
        :param distance:            向量之间相似度的距离度量方法 COSINE: 余弦相似度; EUCLID: 欧几里得距离; DOT: 点积
        """
        self.collection_name = collection_name
        if is_local:
            self.client = QdrantClient(url="http://localhost:6333")
            logger.info(f"连接本地 Qdrant 成功")
        else:
            # 连接线上数据库
            self.client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY"),
            )
            logger.info(f"连接本地 Qdrant Cloud 成功")

        # 判断集合是否存在
        if self.client.collection_exists(collection_name=self.collection_name):
            # 集合存在，直接获取
            self.client.get_collection(self.collection_name)
            logger.info(f"连接已有集合成功, collection_name: {self.collection_name}")
        else:
            # 集合不存在，创建集合
            # self.client.create_collection(
            #     collection_name=self.collection_name,
            #     vectors_config=models.VectorParams(size=dimension, distance=distance),
            # )
            logger.warning(f"连接已有集合失败, collection_name: {self.collection_name}")

    # 查看某个集合信息
    def get_collection(self):
        """
        查看某个集合信息
        :return:
        """
        result = self.client.get_collection(collection_name=self.collection_name)
        return result

    # 检索查询数据
    def search(self, query_vector, limit):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector[0],
            limit=limit
        )
        return search_result

