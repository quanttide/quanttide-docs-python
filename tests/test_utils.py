import tempfile
import unittest

from quanttide_docs.utils import *


class AutodiscoverYamlFileTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.yml_path = os.path.join(self.dir.name, '_config.yml')
        self.yaml_path = os.path.join(self.dir.name, '_config.yaml')

    def tearDown(self) -> None:
        self.dir.cleanup()

    def test_autodiscover_yaml_file_with_only_yml(self):
        with open('_config.yml', 'w') as f:
            pass
        path = autodiscover_yaml_file(self.yml_path)
        self.assertEqual(self.yml_path, path)

    def test_autodiscover_yaml_file_with_only_yaml(self):
        with open('_config.yaml', 'w') as f:
            pass
        path = autodiscover_yaml_file(self.yml_path)
        self.assertEqual(self.yaml_path, path)

    def test_autodiscover_yaml_file_with_both_yml_and_yaml(self):
        with open('_config.yml', 'w') as f1, open('_config.yaml') as f2:
            pass
        with self.assertRaises(Exception, autodiscover_yaml_file(self.yml_path)) as e:
            self.assertEqual('', e.exception)

    def test_autodiscover_yaml_file_without(self):
        with self.assertRaises(Exception, autodiscover_yaml_file(self.yml_path)) as e:
            self.assertEqual('', e.exception)


if __name__ == '__main__':
    unittest.main()
