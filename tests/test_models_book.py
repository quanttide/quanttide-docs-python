import unittest

from quanttide_docs.models.book import Book
from quanttide_docs.config import settings


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.remote_url = settings.TEST_REMOTE_URL

    def test_init(self):
        book = Book(remote_url=self.remote_url)
        self.assertTrue(book)

    def test_context_manager(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertFalse(book.repo.bare)

    def test_get_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.created_at, settings.DATETIME_FORMAT)

    def test_get_updated_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.updated_at, settings.DATETIME_FORMAT)

    def test_get_version_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.get_version_created_at('0.1.0'), settings.DATETIME_FORMAT)

    def test_config(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertTrue(hasattr(book, 'config'))
            print(book.config)


if __name__ == '__main__':
    unittest.main()
