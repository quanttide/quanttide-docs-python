"""
文章领域模型测试
"""
import tempfile
import unittest

from quanttide_docs.models.article import Article
from quanttide_docs.models.git import BookRepo
from quanttide_docs.config import settings


class ArticleTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.repo = BookRepo.clone_from(settings.TEST_REMOTE_URL, to_path=self.dir.name)
        self.path = '01_quick_start/1_hello_world/1_hello_world.md'
        self.blob = self.repo.tree()[self.path]
        self.abspath = self.blob.abspath
        self.commits = self.repo.iter_commits(paths=[self.path])

    def tearDown(self) -> None:
        self.repo.close()
        self.dir.cleanup()

    def test_init(self):
        article = Article(self.abspath, self.commits)
        self.assertTrue(hasattr(article, 'abspath'))

    def test_context_manager(self):
        with Article(self.abspath, self.commits) as article:
            self.assertTrue(hasattr(article, 'raw'))
            print(article.raw)

    def test_name(self):
        with Article(self.abspath, self.commits) as article:
            # 1_hello_world
            self.assertEqual('hello-world', article.name)
            # hello_world
            article.abspath = 'hello_world'
            self.assertEqual('hello-world', article.name)
            # Hello_World
            article.abspath = 'Hello_World'
            self.assertEqual('hello-world', article.name)

    def test_created_at(self):
        with Article(self.abspath, self.commits) as article:
            self.assertRegex(article.created_at, settings.DATETIME_FORMAT)
            print(article.created_at)

    def test_updated_at(self):
        with Article(self.abspath, self.commits) as article:
            self.assertRegex(article.updated_at, settings.DATETIME_FORMAT)
            print(article.updated_at)

    def test_meta(self):
        with Article(self.abspath, self.commits) as article:
            self.assertTrue(hasattr(article, 'meta'))
            print(article.meta)


if __name__ == '__main__':
    unittest.main()
