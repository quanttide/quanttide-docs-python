"""
文章(Article)数据模型
"""

import os.path
from contextlib import AbstractContextManager
from typing import Optional

import markdown


class Article(AbstractContextManager):
    """
    文章数据模型

    假设checkout到某个commit，获取这个commit的文件快照及这个commit以前的所有commit。
    """
    def __init__(self, abspath, commits):
        """

        :param abspath: 文件绝对路径
        :param commits: 文件关联Commit对象，按时间顺序从最近到最远排列
        """
        self.abspath = abspath
        self.commits = tuple(commits)  # generator -> tuple

    def __enter__(self):
        self.fp = open(self.abspath, 'r', encoding='utf-8')
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
        - 大写全部转小写。
        - README文件取所属文件夹名解析。

        Ref:
          - https://www.contentstack.com/docs/developers/create-content-types/understand-default-url-pattern/
        :return: 文章ID。比如`article-name`，来自于文件名`1_article_name`或者`article_name`或者`Article_Name`。
        """
        # README文件取所属文件夹名，非README正常
        path = os.path.dirname(self.abspath) if 'README' in self.abspath else self.abspath
        basename = os.path.splitext(os.path.basename(path))[0]
        splits = basename.split('_', 1)
        return (splits[1] if splits[0].isnumeric() else basename).replace('_', '-').lower()

    @property
    def created_at(self):
        """
        开始被跟踪的提交时间。
        :return:
        """
        first_commit = next(reversed(self.commits))
        return first_commit.committed_datetime.isoformat()

    @property
    def updated_at(self):
        """
        最后编辑的提交时间。
        :return:
        """
        latest_commit = next(iter(self.commits))
        return latest_commit.committed_datetime.isoformat()

    @property
    def meta(self) -> dict:
        """
        解析MyST Markdown文件头部元数据为文章元信息。
        :return:
        """
        md_parser = markdown.Markdown(extensions=['full_yaml_metadata'])
        md_parser.convert(self.raw)
        return md_parser.Meta

    @property
    def title(self) -> Optional[str]:
        """
        解析首个一级标题为文章标题

        比如meta后的第一个有文字的行为`# 输入和输出`，结果为`输入和输出`。
        :return:
        """
        for line in self.raw.split('\n'):
            if line.startswith('#') and line.count('#') == 1:
                return line.replace('# ', '')
        return None

    @property
    def content(self):
        """
        TODO: 根据业务系统需要进行优化
        :return:
        """
        lines = self.raw.split('\n')
        if lines[0] == '---':
            lines_enumerate = enumerate(lines)
            next(lines_enumerate)
            for i, line in lines_enumerate:
                if line in ('---', '...'):
                    lines = lines[i + 1:]
                    break
                if line.startswith('#') and line.count('#') == 1:
                    return '\n'.join(lines[i + 1:])
        for i, line in enumerate(lines):
            if line.startswith('#') and line.count('#') == 1:
                return '\n'.join(lines[i + 1:])
        return self.raw
