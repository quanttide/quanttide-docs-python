"""
文档仓库数据模型
"""

from git import Repo


class BookRepo(Repo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def checkout_version(self, version: str):
        """
        检出文档版本。

        Ref:
          - https://gitpython.readthedocs.io/en/stable/reference.html#git.repo.base.Repo.git
          - https://stackoverflow.com/questions/20073873/how-to-checkout-a-tag-with-gitpython

        :param version: 文档版本，比如`0.1.0`
        :return:
        """
        self.git.checkout(version)

    def log(self, path):
        """

        :param path:
        :return:
        """
        self.git.log(path)
