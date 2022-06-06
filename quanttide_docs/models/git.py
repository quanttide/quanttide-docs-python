"""
文档仓库数据模型
"""

from git import Git, Repo


class BookRepo(Repo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def checkout_version(self, version: str):
        """
        检出文档版本。

        :param version: 文档版本，比如`0.1.0`
        :return:
        """
        # https://stackoverflow.com/questions/20073873/how-to-checkout-a-tag-with-gitpython
        g = Git(self.working_tree_dir)
        g.checkout(version)
