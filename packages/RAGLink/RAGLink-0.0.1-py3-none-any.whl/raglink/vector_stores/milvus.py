#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/3 14:44
# @Author : justin.郑 3907721@qq.com
# @File : milvus.py
# @desc : Milvus 向量数据库操作


from raglink.utils.logger import logger
from raglink.vector_stores.base import VectorStoreBase
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility


class Milvus():
    def __init__(
        self,
        collection_name="raglink",
        vector_size=1536,
        client=None,
        connections_name="default",
        host="localhost",
        port=19530,
        uri=None,
        token=None
    ):
        """
        初始化 Milvus 向量数据库操作类
        :param collection_name:
        :param vector_size:
        :param client:
        :param connections_name:
        :param host:
        :param port:
        :param uri:
        :param token:
        """
        pass
