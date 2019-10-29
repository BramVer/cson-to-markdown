from cson_to_markdown import __version__


def test_version():
    assert __version__ == "0.1.0"


class TestFileConverter:
    def test_it_can_read_the_files(self):
        pass


class TestMarkdownExtractor:
    pass


class TestMarkdownWriter:
    pass


class TestMetadataWriter:
    pass
