from cson_to_markdown.config import Config


class MarkdownBoundsNotFound(Exception):
    pass


class Extractor:
    def __init__(self, cson_content):
        self.config = Config()
        self.content = [l.rstrip("\n") for l in cson_content]

    def _get_markdown_index_boundaries(self):
        try:
            _from = self.content.index(self.config.get("MARKDOWN_START"))
            _to = self.content.index(self.config.get("MARKDOWN_END"))
        except ValueError as verr:
            msg = f"Markdown boundary is missing in content:\n{verr}"
            raise MarkdownBoundsNotFound(msg)

        return _from, _to

    def extract_markdown(self):
        _from, _to = self._get_markdown_index_boundaries()

        markdown = self.content[(_from + 1) : _to]

        return [l.lstrip() for l in markdown]

    def extract_metadata(self):
        _from, _to = self._get_markdown_index_boundaries()

        first_half = self.content[0:_from]
        second_half = self.content[(_to + 1) :]

        return first_half + second_half

    def extract(self):
        return (self.extract_markdown(), self.extract_metadata())

    def _scan_content(self, start, end=None):
        end = end or self.config.get("YAML_STRING_INDICATOR")

        lines = [l for l in self.content if l.startswith(start)]
        if not lines:
            return

        return lines[0].replace(start, "").rstrip(end)

    def get_filename(self, fall_back=None):
        title = self._scan_content(self.config.get("TITLE_INDICATOR"))
        if not title:
            title = f"NOT_FOUND_{fall_back}"
            print(f'Title was not found in content, set to "{title}"')

        return title.lower().replace(" ", "_")

    def get_folder_key(self, fall_back=None):
        return self._scan_content(self.config.get("FOLDER_INDICATOR"))
