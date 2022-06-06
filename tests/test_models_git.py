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
        self.assertEqual('e8f53c9f0521a58eb891cb74ab47c7ec9b96ea27', self.book_repo.head.commit.hexsha)

    def test_log(self):
        result = self.book_repo.log('README.md')
        print(result)


if __name__ == '__main__':
    unittest.main()
