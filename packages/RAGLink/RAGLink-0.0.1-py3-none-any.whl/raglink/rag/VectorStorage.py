#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/6/23 09:52
# @Author : justin.郑 3907721@qq.com
# @File : VectorStorage.py
# @desc : 操作向量存储

import os
from dotenv import load_dotenv
from raglink.utils.config import config
from raglink.utils.logger import logger
from raglink.vector_stores.MilvusDatabase import MilvusDatabase
from raglink.rag.SelectEmbeddings import SelectEmbeddings
from langchain_community.vectorstores import Qdrant

load_dotenv()


class VectorStorage:
    def __init__(self):
        """
        初始化
        """
        self.milvus_config = config.get_milvus_config()
        self.qdrant_config = config.get_qdrant_config()
        self.embeddings_config = config.get_embeddings_config()
        self.database_config = config.get_database_config()

    # 执行
    def run(self, docs, namespace, collection_description=""):
        if self.database_config['database_type'] == "milvus":
            self.run_milvus(docs, namespace, collection_description)
        elif self.database_config['database_type'] == "qdrant":
            self.run_qdrant(docs, namespace)

    # 执行 Qdrant 向量存储
    def run_qdrant(self, docs, namespace):
        try:
            embeddings = SelectEmbeddings().get_embeddings()
            if self.qdrant_config['is_local']:
                Qdrant.from_documents(
                    docs,
                    embeddings,
                    prefer_grpc=True,
                    collection_name=namespace,
                    url="http://localhost:6333/"
                )
            else:
                Qdrant.from_documents(
                    docs,
                    embeddings,
                    prefer_grpc=True,
                    collection_name=namespace,
                    url=os.getenv("QDRANT_URL"),
                    api_key=os.getenv("QDRANT_API_KEY")
                )
            logger.info("Qdrant向量数据存储 完成")
        except Exception as e:
            logger.error(f"Qdrant向量数据存储 失败: {e}")

    # 执行 milvus 向量存储
    def run_milvus(self, docs, namespace, collection_description=""):
        """
        向量化与向量存储
        :param docs:                    要存储的数据列表
        :param dimension:               向量维度
        :param namespace:               分区名称
        :param is_local:                是否链接本地数据 True为本地数据库; False；为zilliz远程数据库
        :param index_type:              索引类型    zilliz 为远程zilliz数据库；attu 本地数据库
        :param collection_description:  集合描述（可选）
        :return:
        """
        # 选择获取Embeddings模型
        embeddings = SelectEmbeddings().get_embeddings()

        data_list = []
        for doc in docs:
            # 使用 BCEmbedding 方式
            if self.embeddings_config['embeddings_model_name'] == "BCEmbedding":
                content_vector = embeddings.encode(doc.page_content)[0]
            else:
                content_vector = embeddings.embed_query(doc.page_content)

            # 使用 LangchainEmbeddings 方式
            # content_vector = embeddings.embed_query(doc.page_content)

            data_list.append(
                {
                    "source": doc.metadata.get("source"),
                    "content": doc.page_content,
                    "content_vector": content_vector
                }
            )

        try:
            milvus_retrieval = MilvusDatabase(
                collection_name=self.milvus_config['collection_name'],
                connections_name=self.milvus_config['connections_name'],
                connections_host=self.milvus_config['connections_host'],
                connections_port=self.milvus_config['connections_port'],
                is_local=self.milvus_config['is_local']
            )
            milvus_retrieval.create_collection(
                collection_description=collection_description,
                dimension=self.embeddings_config['dimension'],
                index_type=self.milvus_config['index_type']
            )
            milvus_retrieval.insert_data_partition(data=data_list, partition_name=namespace)
            logger.info("Milvus向量数据存储 完成")
        except Exception as e:
            logger.error(f"Milvus向量数据存储失败，{e}")


if __name__ == '__main__':
    pass

