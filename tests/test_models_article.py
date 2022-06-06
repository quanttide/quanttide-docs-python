"""
文章领域模型测试
"""
import unittest

from quanttide_docs.models.article import Article
from quanttide_docs.models.git import BookRepo
from quanttide_docs.config import settings


class ArticleTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = BookRepo.clone_from(settings.TEST_REMOTE_URL)

    def test_init(self):
        article = Article(repo=self.repo)


if __name__ == '__main__':
    unittest.main()
