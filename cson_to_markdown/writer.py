import os

import yaml


class BaseWriter:
    def __init__(self, filename, path, content):
        self.filename = filename
        self.path = path
        if isinstance(content, (list, tuple)):
            content = content.join("\n")

        self.content = content

    @property
    def new_path(self):
        return os.path.join(self.path, self.filename)

    def write(self):
        raise NotImplementedError


class MarkdownWriter(BaseWriter):
    def write(self):
        with open(self.new_path, "wb") as f:
            f.write(self.content)


class MetadataWriter(BaseWriter):
    def write(self):
        with open(self.new_path, "wb") as f:
            yaml.dump(self.content, f)
