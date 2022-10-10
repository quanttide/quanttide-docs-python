"""
量潮课堂管理后台命令行工具

```shell
qtdocs <command> <subcommand> <params>
```

本地开发调试
```shell
python3 quanttide_docs.cli.__main__ --help
```

参考资料：
  - https://typer.tiangolo.com
  - https://typer.tiangolo.com/typer-cli/
  - https://mp.weixin.qq.com/s/h1Avhk6FuX375PIySvsqIQ
"""

import typer

from quanttide_docs.cli.tutorial import cli as tutorial_cli


# Typer实例
cli = typer.Typer()
# 添加子命令
# https://typer.tiangolo.com/tutorial/subcommands/add-typer/

# 教程工具
cli.add_typer(tutorial_cli, name='tutorial')


if __name__ == '__main__':
    cli()
