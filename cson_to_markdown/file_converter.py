import os
from pathlib import Path

import attr

from cson_to_markdown.extractor import Extractor
from cson_to_markdown.writer import Writer

CSON_EXTENSION = ".cson"
MARKDOWN_EXTENSION = ".md"
METADATA_EXTENSION = ".yml"
METADATA_SUB_FOLDER = "meta"


@attr.s
class ContentHolder:
    content = attr.ib()
    name = attr.ib()
    extension = attr.ib()

    @property
    def filename(self):
        return f"{self.name}{self.extension}"


class FileConverter:
    def __init__(self, og_path=None, new_path=None):
        self.og_path = og_path
        self.new_path = new_path or self.og_path

    def convert(self):
        self._walk_over_files_in_directory_recursively()

    def _get_basename(self):
        return os.path.basename(self.og_path)

    def _get_all_files_top_down(self):
        cson_pattern = f"*{CSON_EXTENSION}"

        return Path(self.og_path).rglob(cson_pattern)

    def _get_content_from_file(self, path):
        with open(path, "r") as f:
            return f.readlines()

    def _write_new_content(self, holder):
        writer = Writer(holder.filename, self.new_path, holder.content)
        writer.write()

    def _handle_cson_content(self, content):
        extr = Extractor(content)
        basename = extr.get_filename()
        meta_path = os.path.join(METADATA_SUB_FOLDER, basename)

        holders = [
            ContentHolder(extr.extract_markdown(), basename, MARKDOWN_EXTENSION),
            ContentHolder(extr.extract_metadata(), meta_path, METADATA_EXTENSION),
        ]

        for h in holders:
            self._write_new_content(h)

    def _walk_over_files_in_directory_recursively(self):
        recursive_path_generator = self._get_all_files_top_down()

        for path in recursive_path_generator:
            content = self._get_content_from_file(path)

            self._handle_cson_content(content)
