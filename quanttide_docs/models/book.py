"""
书籍(Book)数据模型
"""

import os
import tempfile
from contextlib import AbstractContextManager
from typing import Union, List
from warnings import warn

from git.objects.util import from_timestamp
import yaml

from quanttide_docs.models.article import Article
from quanttide_docs.models.git import BookRepo
from quanttide_docs.models.toc import TOC


class Book(AbstractContextManager):
    """
    书籍数据模型
    """

    def __init__(self, remote_url):
        """
        :param remote_url: Git仓库地址。
        """
        self.remote_url = remote_url
        self.config_path = '_config.yml'
        self.toc_path = '_toc.yml'

    def __enter__(self):
        """
        下载教程仓库到临时文件夹
        :return:
        """
        # 存储仓库的临时文件夹
        # https://docs.python.org/zh-cn/3/library/tempfile.html#tempfile.TemporaryDirectory
        self.dir = tempfile.TemporaryDirectory()
        # clone仓库到临时文件夹
        self.repo = BookRepo.clone_from(self.remote_url, to_path=self.dir.name)
        # config文件
        self.config_abspath = os.path.join(self.dir.name, self.config_path)
        # toc文件
        self.toc_abspath = os.path.join(self.dir.name, self.toc_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> Union[bool, None]:
        """
        关闭上下文管理器

        处理过程：
          1. 清理临时文件夹

        TODO:
          - 完善异常捕获

        :param exc_type:
        :param exc_value:
        :param traceback:
        :return:
          - True: raise
          - False or None: ignore
        """
        # 关闭仓库
        self.repo.close()
        # 显式清理临时文件夹
        self.dir.cleanup()
        return None

    @property
    def created_at(self) -> str:
        """
        定义first commit时间为仓库创建时间。

        :return: ISO格式的时间，比如`2021-04-29T19:01:37+08:00`。
        """
        first_commit = next(self.repo.iter_commits(reverse=True))
        return first_commit.committed_datetime.isoformat()

    def checkout_version(self, version):
        self.repo.git.checkout(version)

    @property
    def updated_at(self) -> str:
        """
        定义latest commit为仓库最近更新时间。

        :return: ISO格式的时间，比如`2021-04-29T19:01:37+08:00`。
        """
        latest_commit = next(self.repo.iter_commits())
        return latest_commit.committed_datetime.isoformat()

    def get_version_created_at(self, version: str):
        """
        获取版本创建时间。定义Git标签创建时间为书籍版本创建时间。

        :param version: 语义化版本格式的Git标签。
        :return: ISO格式的时间，比如`2022-05-27T21:47:55`
        """
        tag_object = self.repo.tag(version).tag
        return from_timestamp(tag_object.tagged_date, tag_object.tagger_tz_offset).isoformat()

    @property
    def config(self) -> dict:
        """
        配置
        :return:
        """
        with open(self.config_abspath) as f:
            config = yaml.safe_load(f)
        return config

    @property
    def toc(self) -> List[dict]:
        # https://stackoverflow.com/questions/9885217/in-python-if-i-return-inside-a-with-block-will-the-file-still-close
        with TOC(self.toc_abspath) as toc_model:
            return toc_model.parse()

    @property
    def articles(self) -> List[dict]:
        """
        文章列表
        :return:
        """
        articles = []
        for item in self.toc:
            file_path = item.pop('file_path')
            file_abspath = os.path.join(self.dir.name, file_path)
            if not os.path.exists(file_abspath):
                warn(f"TOC文件中配置的`{file_path}`不存在，请检查文件配置是否正确。")
                continue
            with Article(file_abspath, self.repo.iter_commits(paths=[file_abspath])) as article_model:
                item.update({'name': article_model.name, 'created_at': article_model.created_at,
                             'updated_at': article_model.updated_at, 'title': article_model.title,
                             'meta': article_model.meta, 'content': article_model.content})
                articles.append(item)
        return articles
