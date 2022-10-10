import unittest

from typer.testing import CliRunner

from quanttide_docs.cli.tutorial import preview
from quanttide_docs.cli.__main__ import cli
from quanttide_docs.config import settings


class PreviewTestCase(unittest.TestCase):
    def test_preview(self):
        preview(settings.TEST_LOCAL_PATH)


class TutorialsCommandsTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_preview_command(self):
        """
        qtclass-admin tutorials preview programming-with-python --path=<local_path>
        :return:
        """
        result = self.runner.invoke(cli, ['tutorials', 'preview', f'--path={settings.TEST_LOCAL_PATH}'])
        self.assertEqual(0, result.exit_code)
        self.assertIn(f'课程名称：{settings.TEST_COURSE_NAME}', result.stdout)


if __name__ == '__main__':
    unittest.main()
