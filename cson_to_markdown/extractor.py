from cson_to_markdown.config import Config


class Extractor:
    def __init__(self, cson_content):
        self.config = Config()
        self.content = [l.rstrip("\n") for l in cson_content]

    def _get_markdown_index_boundaries(self):
        _from = self.content.index(self.config.get("MARKDOWN_START"))
        _to = self.content.index(self.config.get("MARKDOWN_END"))

        return _from, _to

    def extract_markdown(self):
        _from, _to = self._get_markdown_index_boundaries()

        markdown = self.content[(_from + 1) : _to]

        return [l.lstrip() for l in markdown]

    def extract_metadata(self):
        _from, _to = self._get_markdown_index_boundaries()

        first_half = self.content[0:_from]
        second_half = self.content[(_to + 1) : -1]

        return first_half + second_half

    def extract(self):
        return (self.extract_markdown(), self.extract_metadata())

    def get_filename(self):
        line = next(
            l for l in self.content if l.startswith(self.config.get("TITLE_INDICATOR"))
        )

        title = line.replace(self.config.get("TITLE_INDICATOR"), "").rstrip(
            self.config.get("TITLE_END_CHAR")
        )

        return title.lower().replace(" ", "_")
