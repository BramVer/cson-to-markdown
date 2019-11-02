from fire import Fire

from cson_to_markdown.file_converter import FileConverter

__version__ = "0.1.0"


def _convert(og_path, new_path=None, settings_dir=None):
    start_msg = f'Start .cson to .md conversion on "{og_path}".'
    print(start_msg)

    converter = FileConverter(og_path, new_path, settings_dir)
    converter.convert()

    end_msg = f'Successfully converted files to "{new_path or og_path}".'
    print(end_msg)


def main():
    Fire(_convert)
