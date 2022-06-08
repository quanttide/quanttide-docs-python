# 用户文档

## Usage

使用上下文管理器来处理，比如：

```python
with Book(name=name) as book:
    book.parse()
```