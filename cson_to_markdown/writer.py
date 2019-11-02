import os


class Writer:
    def __init__(self, filename, path, content):
        self.filename = filename
        self.path = path
        self.content = content

        self._create_path_if_not_exists()

    @property
    def new_path(self):
        return os.path.join(self.path, self.filename)

    def join_content(self, glue):
        return glue.join(self.content)

    def _create_path_if_not_exists(self):
        path = os.path.dirname(self.new_path)
        if not os.path.exists(path):
            os.makedirs(path)

    def write(self):
        content = self.join_content("\n")

        with open(self.new_path, "w") as f:
            f.write(content)
