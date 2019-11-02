import os

import pytest

from cson_to_markdown import __version__
from cson_to_markdown.extractor import Extractor
from cson_to_markdown.file_converter import FileConverter
from cson_to_markdown.writer import Writer


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def metadata_content():
    metadata_start = [
        "This line is metadata",
        "so is this line.",
        " this will not trigger first boundary ---:",
        "---: neither will this",
        "---:",
    ]
    metadata_end = [
        ":---",
        "this line marks end of markdown and will not be shown again!",
        "This is yet again metadata",
        "T:  ZIS IS ze TIT_EL!!_WHICH_will_get_formaTTTErd",
        ":--- noone cares about this boundary",
    ]

    return metadata_start, metadata_end


@pytest.fixture
def markdown_content():
    markdown = [
        "This is markdown",
        "so is this",
        "---:",
        "I can put a first boundary in this one w/out being triggered",
        "and even an end boundary :---",
    ]

    return markdown


class TestExtractor:
    def test_it_extracts_content_between_boundaries(
        self, monkeypatch, metadata_content, markdown_content
    ):
        monkeypatch.setenv("MARKDOWN_START", "---:")
        monkeypatch.setenv("MARKDOWN_END", ":---")

        markdown = markdown_content
        metadata_start, metadata_end = metadata_content

        expected_markdown = markdown
        expected_metadata = metadata_start[:-1] + metadata_end[1:]

        extr = Extractor(metadata_start + markdown + metadata_end)
        actual_markdown = extr.extract_markdown()
        actual_metadata = extr.extract_metadata()

        assert expected_markdown == actual_markdown
        assert expected_metadata == actual_metadata

    def test_it_gets_and_formats_title_from_the_content(
        self, monkeypatch, metadata_content
    ):
        monkeypatch.setenv("TITLE_INDICATOR", "T:  ")

        _, content = metadata_content

        expected_title = "zis_is_ze_tit_el!!_which_will_get_formattterd"

        extr = Extractor(content)
        actual_title = extr.get_filename()

        assert expected_title == actual_title


class TestWriter:
    def test_it_creates_path_if_not_pressent(self, monkeypatch, tmpdir):
        new_dir = "meta"
        new_path = os.path.join(tmpdir, new_dir)
        fname = "new_file.txt"
        content = ["Henlo", "!!"]

        assert not os.path.exists(new_path)

        writer = Writer(fname, new_path, content)
        writer.write()

        assert os.path.exists(new_path)
        with open(os.path.join(new_path, fname)) as f:
            assert f.read() == f"{content[0]}\n{content[1]}"


class TestFileConverter:
    def test_it_walks_files_and_handles_content(
        self, monkeypatch, tmpdir, metadata_content, markdown_content
    ):
        monkeypatch.setenv("TITLE_INDICATOR", "Title:  ")
        monkeypatch.setenv("MARKDOWN_START", "---:")
        monkeypatch.setenv("MARKDOWN_END", ":---")

        og_path = tmpdir
        new_path = os.path.join(tmpdir, "MARKDOWN_FILES")

        meta_start, meta_end = metadata_content
        markdown_content = markdown_content
        content = "\n".join(meta_start + markdown_content + meta_end)

        for i in range(5):
            file = og_path.join(f"file_{i}.cson")
            file.write(f"{content}\nTitle:  new_title {i}")

        converter = FileConverter(og_path, new_path)
        converter.convert()

        new_files = [
            i
            for i in os.listdir(new_path)
            if not os.path.isdir(os.path.join(new_path, i))
        ]

        assert len(new_files) == 5
        assert new_files[0][-3:] == ".md"
