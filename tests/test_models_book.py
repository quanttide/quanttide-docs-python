import unittest

from quanttide_docs.models.book import Book
from quanttide_docs.config import settings


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.remote_url = settings.TEST_REMOTE_URL
        self.local_path = settings.TEST_LOCAL_PATH

    def test_init_remote(self):
        book = Book(remote_url=self.remote_url)
        self.assertTrue(book)

    def test_init_local(self):
        book = Book(local_path=self.local_path)
        self.assertTrue(book)

    def test_init_error(self):
        with self.assertRaises(ValueError) as e:
            book = Book()
        with self.assertRaises(ValueError) as e:
            book = Book(remote_url=self.remote_url, local_path=self.local_path)

    def test_context_manager(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertFalse(book.repo.bare)

    def test_context_manager_for_local(self):
        with Book(local_path=self.local_path) as book:
            self.assertFalse(book.repo.bare)

    def test_checkout_version(self):
        with Book(remote_url=self.remote_url) as book:
            book.checkout_version('0.1.0')
            # https://gitpython.readthedocs.io/en/stable/reference.html#git.refs.head.Head
            self.assertEqual('e8f53c9f0521a58eb891cb74ab47c7ec9b96ea27', book.repo.head.commit.hexsha)

    def test_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.created_at, settings.DATETIME_FORMAT)

    def test_updated_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.updated_at, settings.DATETIME_FORMAT)

    def test_get_version_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.get_version_created_at('0.1.0'), settings.DATETIME_FORMAT)

    def test_config(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertTrue(hasattr(book, 'config'))
            print(book.config)

    def test_articles(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertTrue(hasattr(book, 'articles'))
            print(book.articles)


if __name__ == '__main__':
    unittest.main()
