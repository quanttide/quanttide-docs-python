"""
TOC领域模型
"""

from contextlib import AbstractContextManager

import yaml


class TOC(AbstractContextManager):
    def __init__(self, abspath):
        self.abspath = abspath

    def __enter__(self):
        self.fp = open(self.abspath, 'r')
        self.raw_data = yaml.safe_load(self.fp)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fp.close()
        return None

    def generate_course_content_item(self, part_no=None, chapter_no=None, section_no=None, subsection_no=None,
                                     file_path=None):
        is_readme = 'README' in file_path
        return dict(part_no=part_no, chapter_no=chapter_no, section_no=section_no, subsection_no=subsection_no,
                    is_readme=is_readme, file_path=file_path)

    def parse_sections(self, sections: list, chapter_no, part_no=None):
        result = []
        for i, section in enumerate(sections):
            section_no = i + 1
            result.append(self.generate_course_content_item(part_no=part_no, chapter_no=chapter_no, section_no=section_no,
                                                            file_path=section['file']))
        return result

    def parse_chapters(self, chapters: list, part_no=None, chapter_no_add=0):
        result = []
        for i, chapter in enumerate(chapters):
            chapter_no = i + 1 + chapter_no_add
            result.append(
                self.generate_course_content_item(part_no=part_no, chapter_no=chapter_no, file_path=chapter['file'])
            )
            if 'sections' in chapter:
                result.extend(self.parse_sections(chapter['sections'], chapter_no))
        return result

    def parse_parts(self, parts: list):
        result = []
        chapter_no_add = 0
        for i, part in enumerate(parts):
            part_no = i + 1
            if 'chapters' in part:
                result.extend(
                    self.parse_chapters(part['chapters'], part_no, chapter_no_add)
                )
                chapter_no_add += len(part['chapters'])
        return result

    def parse(self):
        if 'chapters' in self.raw_data:
            return self.parse_chapters(self.raw_data['chapters'])
        elif 'parts' in self.raw_data:
            return self.parse_parts(self.raw_data['parts'])
        else:
            raise ValueError("TOC文件格式错误")
