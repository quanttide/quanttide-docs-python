import unittest
from pprint import pprint

from quanttide_docs.models.tutorial import Tutorial
from quanttide_docs.config import settings


class TutorialsTestCase(unittest.TestCase):
    def setUp(self):
        self.remote_url = settings.TEST_REMOTE_URL
        self.local_path = settings.TEST_LOCAL_PATH

    def test_init_from_coding_devops(self):
        book = Tutorial.init_from_coding_devops(project_name=settings.TEST_CODING_PROJECT_NAME, depot_name=settings.TEST_CODING_DEPOT_NAME, username=settings.TEST_GIT_USERNAME, password=settings.TEST_GIT_PASSWORD)
        self.assertEqual(self.remote_url, book.remote_url)

    def test_init_from_local(self):
        book = Tutorial.init_from_local_repo(local_path=self.local_path)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            book = Tutorial()
        with self.assertRaises(ValueError):
            book = Tutorial(remote_url=self.remote_url, local_path=self.local_path)

    def test_is_valid(self):
        with Tutorial(local_path=self.local_path) as tutorials:
            tutorials.checkout_version('0.1.1')
            self.assertTrue(tutorials.is_valid())

    def test_to_dict(self):
        with Tutorial(local_path=self.local_path) as tutorials:
            course_version = tutorials.to_dict(version='0.1.1')
            pprint(course_version)

    def test_to_dict_without_content(self):
        with Tutorial(local_path=self.local_path) as tutorials:
            course_version = tutorials.to_dict(version='0.1.1', with_content=False)
            pprint(course_version)

    def test_to_dict_for_head(self):
        """
        HEAD指向的commit，通常是最新的commit。
        用于本地检查。
        """
        with Tutorial(local_path=self.local_path) as tutorials:
            course_version = tutorials.to_dict()
            pprint(course_version)


if __name__ == '__main__':
    unittest.main()
