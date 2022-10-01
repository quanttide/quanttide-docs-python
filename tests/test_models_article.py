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
        self.path = '1_example_chapter/1_example_section/1_example_article.md'
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

    def test_name(self):
        with Article(self.abspath, self.commits) as article:
            # 1_hello_world
            self.assertEqual('example-article', article.name)
            # hello_world
            article.abspath = 'hello_world'
            self.assertEqual('hello-world', article.name)
            # Hello_World
            article.abspath = 'Hello_World'
            self.assertEqual('hello-world', article.name)
            # README.md
            article.abspath = '1_hello_world/README.md'
            self.assertEqual('hello-world', article.name)

    def test_created_at(self):
        with Article(self.abspath, self.commits) as article:
            self.assertRegex(article.created_at, settings.DATETIME_FORMAT)
            self.assertEqual(article.created_at, '2022-09-30T17:18:10+08:00')

    def test_updated_at(self):
        with Article(self.abspath, self.commits) as article:
            self.assertRegex(article.updated_at, settings.DATETIME_FORMAT)
            self.assertEqual(article.updated_at, '2022-09-30T17:18:10+08:00')

    def test_meta(self):
        with Article(self.abspath, self.commits) as article:
            self.assertTrue(hasattr(article, 'meta'))
            self.assertEqual(article.meta['level'], 'introductory')
            self.assertEqual(article.meta['stage'], 'alpha')

    def test_title(self):
        with Article(self.abspath, self.commits) as article:
            self.assertTrue(article.title)
            self.assertEqual(article.title, '测试文章')


if __name__ == '__main__':
    unittest.main()
