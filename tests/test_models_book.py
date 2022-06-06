import unittest

from quanttide_docs.models.book import Book
from quanttide_docs.config import settings


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.remote_url = settings.TSET_REMOTE_URL

    def test_init(self):
        book = Book(remote_url=self.remote_url)
        self.assertEqual(f"qtclass-tutorials-{self.course_name}", book.depot_name)

    def test_context_manager(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertFalse(book.repo.bare)

    def test_get_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertEqual('2021-04-29T19:01:37+08:00', book.created_at)

    def test_get_updated_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertEqual('', book.updated_at)

    def test_get_version_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertEqual('', book.get_version_created_at('0.1.0'))


if __name__ == '__main__':
    unittest.main()
