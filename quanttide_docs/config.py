# -*- coding: utf-8 -*-

from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=['settings.toml'],
    environments=True,
    envvar_prefix='QTDOCS',
    load_dotenv=True,
)
