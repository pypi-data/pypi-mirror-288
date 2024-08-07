#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/6/23 15:21
# @Author : justin.郑 3907721@qq.com
# @File : GetContext.py
# @desc : 获得上下文内容


from raglink.utils.config import config
from raglink.utils.logger import logger
from raglink.vector_stores.MilvusDatabase import MilvusDatabase
from raglink.vector_stores.QdrantDatabase import QdrantDatabase
from raglink.rag.SelectEmbeddings import SelectEmbeddings


def _format_qdrant_docs(docs):
    res = ""
    for x in docs:
        res += "\n\n" + x.payload["page_content"]
    return res


def _format_docs(docs):
    res = ""
    for x in docs[0]:
        res += "\n\n" + x.entity.get("content")
    return res


def _format_list(docs):
    res_list = []
    for x in docs[0]:
        res_list.append(x.entity.get("content"))
    return res_list


class GetContext:
    def __init__(self):
        self.milvus_config = config.get_milvus_config()
        self.qdrant_config = config.get_qdrant_config()
        self.database_config = config.get_database_config()
        self.embeddings_config = config.get_embeddings_config()

    def run(self, question, namespace, is_reranker=False):
        """
        获得上下文内容 及 RerankerModel处理
        :param question:    问题
        :param namespace:   命名分区空间
        :param top_k:       返回的最大数量
        :return:
        """
        # 选择获取Embeddings模型
        embeddings = SelectEmbeddings().get_embeddings()

        # 使用 BCEmbedding 方式
        if self.embeddings_config['embeddings_model_name'] == "BCEmbedding":
            question_vector = embeddings.encode(question)
        else:
            question_vector = [embeddings.embed_query(question)]

        # 使用 LangchainEmbeddings 方式
        # question_vector = [embeddings.embed_query(question)]

        # 检索 Qdrant
        if self.database_config['database_type'] == "qdrant":
            res_vec = QdrantDatabase(
                collection_name=namespace,
                is_local=self.qdrant_config['is_local']
            ).search(
                query_vector=question_vector,
                limit=self.embeddings_config['embeddings_top_k']
            )
            # 只执行Embeddings
            context = _format_qdrant_docs(res_vec)
            logger.info(f"GetContext Qdrant 执行Embeddings获取的内容：{context}")
            return context

        # 检索 Milvus
        if self.database_config['database_type'] == "milvus":
            res_vec = MilvusDatabase(
                        collection_name=self.milvus_config['collection_name'],
                        is_local=self.milvus_config['is_local']
                    ).search_data_partition(
                        data=question_vector,
                        partition_name=namespace,
                        top_k=self.embeddings_config['embeddings_top_k']
                    )
            if res_vec is None:
                logger.warning("GetContext milvus 检索不到内容，请检查数据是否正确")
                return ""

            if is_reranker:
                # 执行Embeddings后再执行Reranker
                passages = _format_list(res_vec)
                logger.info(f"GetContext milvus 先执行Embeddings获取的内容")
                context = self.get_reranker(question, passages)
                logger.info(f"GetContext milvus 再执行Reranker获取内容：{context}")
                return context
            else:
                # 只执行Embeddings
                context = _format_docs(res_vec)
                logger.info(f"GetContext milvus 执行Embeddings获取的内容：{context}")
                return context

    # 获取rerank段落
    def get_reranker(self, question, passages):
        reranker_model = SelectEmbeddings().get_reranker()
        rerank_results = reranker_model.rerank(question, passages)
        rerank_passages = rerank_results['rerank_passages'][:self.embeddings_config['reranker_top_k']]
        res = ""
        for x in rerank_passages:
            res += "\n\n" + x
        return res

