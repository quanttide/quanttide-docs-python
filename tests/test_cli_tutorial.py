import unittest

from typer.testing import CliRunner

from quanttide_docs.cli.tutorial import validate, preview
from quanttide_docs.cli.__main__ import cli
from quanttide_docs.config import settings


class ValidateTestCase(unittest.TestCase):
    def test_validate(self):
        validate(settings.TEST_LOCAL_PATH)


class PreviewTestCase(unittest.TestCase):
    def test_preview(self):
        preview(settings.TEST_LOCAL_PATH)


class TutorialsCommandsTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_validate_command(self):
        """
        qtdocs tutorials preview --path=<local_path>
        """
        result = self.runner.invoke(cli, ['tutorials', 'validate', f'--path={settings.TEST_LOCAL_PATH}'])
        self.assertEqual(0, result.exit_code)
        self.assertIn(f'课程名称：{settings.TEST_COURSE_NAME}', result.stdout)

    def test_preview_command(self):
        """
        qtdocs tutorials preview --path=<local_path>
        """
        result = self.runner.invoke(cli, ['tutorials', 'preview', f'--path={settings.TEST_LOCAL_PATH}'])
        self.assertEqual(0, result.exit_code)
        self.assertIn(f'课程名称：{settings.TEST_COURSE_NAME}', result.stdout)


if __name__ == '__main__':
    unittest.main()
