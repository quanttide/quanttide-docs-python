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

    @unittest.skip('TODO: 补充验证正则')
    def test_get_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertRegex(book.created_at, r'')

    def test_get_updated_at(self):
        with Book(remote_url=self.remote_url) as book:
            # TODO: 改为验证格式
            self.assertEqual('2022-05-27T21:47:09+08:00', book.updated_at)

    def test_get_version_created_at(self):
        with Book(remote_url=self.remote_url) as book:
            self.assertEqual('2022-05-27T21:47:55+08:00', book.get_version_created_at('0.1.0'))


if __name__ == '__main__':
    unittest.main()
