import os
import tempfile
import unittest
from pprint import pprint

from quanttide_docs.config import settings
from quanttide_docs.models.git import BookRepo
from quanttide_docs.models.toc import TOC


class TOCTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.repo = BookRepo.clone_from(settings.TEST_REMOTE_URL, to_path=self.dir.name)
        self.path = '_toc.yml'
        self.abspath = os.path.join(self.dir.name, self.path)

    def tearDown(self) -> None:
        self.repo.close()
        self.dir.cleanup()

    def test_init(self):
        toc = TOC(self.abspath)
        self.assertTrue(hasattr(toc, 'abspath'))

    def test_context_manager(self):
        with TOC(self.abspath) as toc:
            self.assertTrue(hasattr(toc, 'raw_data'))

    def test_parse(self):
        with TOC(self.abspath) as toc:
            result = toc.parse()
            self.assertTrue(result)
            pprint(result)


if __name__ == '__main__':
    unittest.main()
