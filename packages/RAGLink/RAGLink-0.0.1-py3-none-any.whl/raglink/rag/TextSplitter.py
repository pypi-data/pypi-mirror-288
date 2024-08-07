#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/6/21 下午2:49
# @Author : justin.郑 3907721@qq.com
# @File : TextSplitter.py
# @desc : 文本内容切割类

"""
- separator：定义文本块之间的分隔符。 默认为："\n\n"  或  ["\n\n", "\n", " ", ""]
- chunk_size：意味着每个块将尽可能接近这个字符长度
- chunk_overlap：表示块之间将有最多重叠的字符数，以保证文本之间的平滑过渡。
- length_function：用于测量文本块大小的函数，这里使用len函数直接计算字符数。
- is_separator_regex：指定separator是否作为正则表达式处理，默认为：False
"""

from raglink.utils.logger import logger
from raglink.rag.DocumentLoaders import DocumentLoaders
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


class TextSplitter:
    def __init__(self):
        pass

    def run(self,
            file_content,
            chunk_size,
            chunk_overlap,
            text_splitter_class="RecursiveCharacterTextSplitter",
            separator=None,
            is_separator_regex=False
            ):
        """
        文本内容切割
        :param file_content:    文本内容
        :param chunk_size:  切割每块的大致长度
        :param chunk_overlap:   块之间将有最多重叠的字符数
        :param text_splitter_class: 指定使用的TextSplitter类
        :param separator:   定义文本块之间的分隔符
        :param is_separator_regex:  指定separator是否作为正则表达式处理
        :return:
        """
        if file_content != None:
            if text_splitter_class == "RecursiveCharacterTextSplitter":
                if separator == None:
                    separator = ["\n\n", "\n", " ", ""]
                text_split = RecursiveCharacterTextSplitter(
                    separators=separator,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    length_function=len,
                    is_separator_regex=is_separator_regex
                )
                result = text_split.split_documents(file_content)
                logger.info(f"TextSplitter 执行 RecursiveCharacterTextSplitter 切割文档，切割{len(result)}块")
                return result

            if text_splitter_class == "CharacterTextSplitter":
                if separator == None:
                    separator = "\n\n"
                text_split = CharacterTextSplitter(
                    separator=separator,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    length_function=len,
                    is_separator_regex=is_separator_regex
                )
                result = text_split.split_documents(file_content)
                logger.info(f"TextSplitter 执行 CharacterTextSplitter 切割文档，切割{len(result)}块")
                return result

        logger.warning("TextSplitter 没有需要切割的文档")


if __name__ == "__main__":
    file_path = "../data/iPhone14.txt"
    file_content = DocumentLoaders().run(file_path)

    res = TextSplitter().run(
        file_content=file_content,
        text_splitter_class="CharacterTextSplitter",
        chunk_size=500,
        chunk_overlap=20
    )
    print(res)

