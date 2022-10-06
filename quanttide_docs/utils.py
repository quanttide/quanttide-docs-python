"""
工具函数
"""

import os


def autodiscover_yaml_file(path: str, name: str) -> str:
    """
    :param path:
    :param name:
    :return filename:
    """
    yml_path, yaml_path = os.path.join(path, name + '.yml'), os.path.join(path, name + '.yaml')
    is_yml_exists, is_yaml_exists = os.path.exists(yml_path), os.path.exists(yaml_path)
    if is_yml_exists:
        if is_yaml_exists:
            raise LookupError(f"both '{name}.yml' and '{name}.yaml' files found")
        return yml_path
    if is_yaml_exists:
        return yaml_path
    raise FileNotFoundError(f"neither '{name}.yml' nor '{name}.yaml' file found")
