"""
文章(Article)数据模型
"""
from contextlib import AbstractContextManager


class Article(AbstractContextManager):
    """
    文章数据模型
    """
    def __init__(self, blob):
        self.blob = blob

    def __enter__(self):
        self.fp = open(self.blob.abspath, 'r')
        self.raw = self.fp.read()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fp.close()
        return None

    @property
    def name(self) -> str:
        """
        文章名称。
        - 作为唯一性标识。
        - 解析文件名并转为URL格式，用作URLPattern的拼接。

        Ref:
          - https://www.contentstack.com/docs/developers/create-content-types/understand-default-url-pattern/
        :return: 文章ID。比如`article-name`，来自于文件名`1_article_name`或者`article_name`。
        """
        splits = self.blob.path.split('_', 1)
        return (splits[1] if splits[0].isnumeric() else self.path).replace('_', '-')

    @property
    def created_at(self):
        """
        开始被跟踪的提交时间。
        :return:
        """
        pass

    @property
    def updated_at(self):
        """
        最后编辑的提交时间。
        :return:
        """
        pass
