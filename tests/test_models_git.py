"""
Git数据模型测试
"""
import unittest
import tempfile

from quanttide_docs.models.git import BookRepo
from quanttide_docs.config import settings


class BookRepoTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.book_repo = BookRepo.clone_from(settings.TEST_REMOTE_URL, to_path=self.dir.name)

    def tearDown(self) -> None:
        self.dir.cleanup()

    def test_checkout_version(self):
        self.book_repo.checkout_version('0.1.0')
        # https://gitpython.readthedocs.io/en/stable/reference.html#git.refs.head.Head
        self.assertEqual('545e05c0a3a255afa0c69c4b2fd6734940517171', self.book_repo.head.commit.hexsha)


if __name__ == '__main__':
    unittest.main()
