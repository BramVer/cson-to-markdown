from fire import Fire

from cson_to_markdown.file_converter import FileConverter

__version__ = "0.1.0"


def _convert(og_path, new_path=None):
    converter = FileConverter(og_path, new_path)
    converter.convert()


def main():
    Fire(_convert)
