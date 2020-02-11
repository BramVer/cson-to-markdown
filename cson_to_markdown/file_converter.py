import json
import os
from pathlib import Path

import attr

from cson_to_markdown.config import Config
from cson_to_markdown.extractor import Extractor, MarkdownBoundsNotFound
from cson_to_markdown.writer import Writer


@attr.s
class ContentHolder:
    content = attr.ib()
    name = attr.ib()
    extension = attr.ib()

    @property
    def filename(self):
        return f"{self.name}{self.extension}"


class FileConverter:
    def __init__(self, og_path, new_path=None, settings_dir=None):
        self.config = Config()

        self.og_path = og_path
        self.new_path = new_path or self.og_path

        self.folder_mapping = self._get_folder_mapping(settings_dir)

    def convert(self):
        self._walk_over_files_in_directory_recursively()

    def _get_folder_mapping(self, root_dir=None):
        mapping = {}
        _dir = root_dir or self.og_path

        path = os.path.join(_dir, self.config.get("BNOTE_SETTINGS_FILE"))
        if not os.path.exists(path):
            return mapping

        with open(path, "r") as dt:
            data = json.load(dt)

            for f in data.get("folders", []):
                mapping[f["key"]] = f["name"]

        return mapping

    def _get_all_files_top_down(self):
        cson_pattern = f"*{self.config.get('CSON_EXTENSION')}"

        return Path(self.og_path).rglob(cson_pattern)

    def _get_content_from_file(self, path):
        with open(path, "r") as f:
            return f.readlines()

    def _write_new_content(self, holder):
        writer = Writer(holder.filename, self.new_path, holder.content)
        writer.write()

    def _handle_cson_content(self, content):
        extr = Extractor(content)
        base_name = extr.get_filename()

        try:
            markdown = extr.extract_markdown()
            metadata = extr.extract_metadata()
        except MarkdownBoundsNotFound:
            print(f"Could not find MD boundaries for file {base_name}.")
            return

        folder_name = self.folder_mapping.get(extr.get_folder_key(), "")
        file_name = os.path.join(folder_name, base_name)
        meta_name = os.path.join(
            folder_name, self.config.get("METADATA_FOLDER"), base_name
        )

        holders = [
            ContentHolder(markdown, file_name, self.config.get("MARKDOWN_EXTENSION")),
            ContentHolder(metadata, meta_name, self.config.get("METADATA_EXTENSION")),
        ]
        for h in holders:
            self._write_new_content(h)

    def _walk_over_files_in_directory_recursively(self):
        recursive_path_generator = self._get_all_files_top_down()

        for path in recursive_path_generator:
            content = self._get_content_from_file(path)

            self._handle_cson_content(content)
