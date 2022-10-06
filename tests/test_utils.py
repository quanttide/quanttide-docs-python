import tempfile
import unittest
import os

from quanttide_docs.utils import *


class AutodiscoverYamlFileTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.yml_path = os.path.join(self.dir.name, '_config.yml')
        self.yaml_path = os.path.join(self.dir.name, '_config.yaml')

    def tearDown(self) -> None:
        self.dir.cleanup()

    def test_autodiscover_yaml_file_with_only_yml(self):
        with open(self.yml_path, 'w'):
            pass
        path = autodiscover_yaml_file(self.dir.name, '_config')
        self.assertEqual(self.yml_path, path)

    def test_autodiscover_yaml_file_with_only_yaml(self):
        with open(self.yaml_path, 'w'):
            pass
        path = autodiscover_yaml_file(self.dir.name, '_config')
        self.assertEqual(self.yaml_path, path)

    def test_autodiscover_yaml_file_with_both_yml_and_yaml(self):
        with open(self.yml_path, 'w'), open(self.yaml_path, 'w'):
            pass
        with self.assertRaises(LookupError) as e:
            autodiscover_yaml_file(self.dir.name, '_config')
        self.assertEqual("both '_config.yml' and '_config.yaml' files found", e.exception.args[0])

    def test_autodiscover_yaml_file_without(self):
        with self.assertRaises(FileNotFoundError) as e:
            autodiscover_yaml_file(self.dir.name, '_config')
        self.assertEqual("neither '_config.yml' nor '_config.yaml' file found", e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
