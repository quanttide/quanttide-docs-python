# CHANGELOG

## [v0.4.0] - 2023-01-

增加图片语法解析。

### Features

领域模型：
- `Article`增加`images`属性。

## [v0.3.0] - 2022-10-10

增加命令行工具。

### Features

数据模型：
- 教程模型`Tutorial`增加`validate`方法
- 教程模型验证逻辑增加验证`name`属性、`title`属性

命令行：
- 增加命令行入口。
- 增加教程格式验证命令`qtdocs tutorial validate`。
- 增加教程格式解析和预览命令`qtdocs tutorial preview`。

## [v0.2.1] - 2022-10-10

优化教程模型。

### Features

- 增加YAML文件自动发现。
- 增加`Article`类入参验证。

## [v0.2.0] - 2022-10-03

增加教程模型`Tutorial`。

## [v0.1.0] - 2022-07-04

最小可用版本。

## Features

- 增加领域模型`Book`、`Article`、 `TOC`。