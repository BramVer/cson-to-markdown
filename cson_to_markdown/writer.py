import os


class BaseWriter:
    def __init__(self, filename, path, content):
        self.filename = filename
        self.path = path
        self.content = content

    @property
    def new_path(self):
        return os.path.join(self.path, self.filename)

    def join_content(self, glue):
        return glue.join(self.content)

    def write(self):
        raise NotImplementedError


class MarkdownWriter(BaseWriter):
    def write(self):
        content = self.join_content("\n")

        with open(self.new_path, "w") as f:
            f.write(content)


class MetadataWriter(BaseWriter):
    def _create_meta_path(self):
        meta_path = os.path.dirname(self.new_path)
        if not os.path.exists(meta_path):
            os.mkdir(meta_path)

    def write(self):
        content = self.join_content("\n")
        self._create_meta_path()

        with open(self.new_path, "w") as f:
            f.write(content)
