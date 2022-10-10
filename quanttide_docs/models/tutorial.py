"""
教程领域模型
"""
from typing import Optional
from collections import Counter
from warnings import warn

from quanttide_docs.models.book import Book


class Tutorial(Book):
    """
    教程数据模型
    """
    def validate(self):
        # 验证`name`非空
        if not self.name:
            raise ValueError('教程名称不可为空，请配置_config.yml文件的name属性。')
        if self.config.get('category') != 'tutorial':
            # TODO：未来换成raise。
            warn(f"文档分类不是教程（tutorial），请设置。")
        # 验证文章
        for article in self.articles:
            # 验证标题存在
            if not article['title']:
                raise ValueError('教程文章标题不可为空。')
        # 验证`lecture_name`唯一
        lecture_names = [article['name'] for article in self.articles]
        if len(set(lecture_names)) < len(lecture_names):
            counter = Counter(lecture_names)
            duplicated_lecture_names = [k for k, v in counter.items() if v > 1]
            raise ValueError(f"{duplicated_lecture_names}存在重复，请检查文件和文件夹命名。")

    def is_valid(self) -> bool:
        self.validate()
        return True

    def to_dict(self, version: Optional[str] = None, with_content=True):
        """
        ```python
        with Tutorial(name='programming-with-python') as tutorials:
            tutorials.to_dict(version='0.1.0')
        ```
        :param version: 语义化版本号，默认为当前head。
        :param with_content: 是否包括正文，默认为True，False用于命令行工具。
        :return:
        """
        # 课程
        course = {key: value for key, value in self.config.items() if
                  key in ['name', 'title', 'author', 'description', 'level', 'stage', 'tags']}
        course['created_at'] = self.created_at
        if not version:
            course['version'] = self.repo.commit().hexsha  # commit id代替
            course['updated_at'] = self.repo.commit().committed_datetime.isoformat()  # commit时间代替
        else:
            course['version'] = version
            course['updated_at'] = self.get_version_created_at(version)
            self.checkout_version(version)  # 解析课时时使用
        # 课时
        course['lectures'] = []
        for article in self.articles:
            lecture = {key: value for key, value in article.items() if
                       key in ['name', 'part_no', 'chapter_no', 'section_no', 'subsection_no', 'is_readme', 'created_at', 'updated_at', 'title']}
            if article['meta']:
                lecture.update(
                    {key: value for key, value in article['meta'].items() if key in ['level', 'stage']})
            if with_content:
                lecture['content'] = article['content']
            course['lectures'].append(lecture)
        return course
