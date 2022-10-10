# -*- coding: utf-8 -*-
import json
import subprocess
import os

import typer

cli = typer.Typer()

from quanttide_docs.models.tutorial import Tutorial


@cli.command()
def preview(path='.'):
    """
    预览当前提交的解析结果。

    :param name: 课程名称，必填。
    :param path: 本地仓库路径，默认为当前目录
    :param result_path: 解析结果存储路径，默认为_build目录的qtclass.json
    :return:
    """
    # 构建兼验证
    subprocess.call(f"jupyter-book build {path}", shell=True)
    # 自定义验证
    with Tutorial(local_path=path) as tutorial:
        # 基础信息
        typer.echo(f"课程名称：{tutorial.name}")
        if hasattr(tutorial, 'depot_name') and tutorial.depot_name:
            typer.echo(f"课程仓库名称：{tutorial.depot_name}")
        if hasattr(tutorial, 'local_path') and tutorial.local_path:
            typer.echo(f"本地仓库位置：{tutorial.local_path}")
        # 解析
        if tutorial.is_valid():
            result = tutorial.to_dict(with_content=False)
            # 保存解析结果用以预览
            # TODO: 改善json文件格式，类似pprint效果、字符编码处理。
            result_path = os.path.join(path, '_build/qtclass.json')
            typer.echo(f"预览解析数据：{result_path}")
            with open(result_path, 'w') as f:
                json.dump(result, f)


@cli.command()
def deploy():
    pass


if __name__ == '__main__':
    cli()
