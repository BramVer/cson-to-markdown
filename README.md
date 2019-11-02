# Cson To Markdown

## What
Recursively scans given folder for `.cson` files, extracts the metadata and markdown,
and writes a `.md` file and a `meta/.yml` file.
Written specifically for use with [Boostnote](https://github.com/BoostIO/Boostnote).

## Why?
I write everything in Markdown format because I like the formatting, and my favourite markdown editor so far is Boostnote.
Everything is stored in a dedicated git repository and pushed whenever changes occur.
This works great!

*The problem* though, is that Boostnote stores the file in a `cson` format, without subfolders  and without legible note-titles.
I wrote something that extracts this information without disturbing the original files, and writes both the markdown and the metadata somewhere else.
They're created in the subfolder to which they belong in the application, with the note title as filename.

**Caution:** A new version is in the works and will be announced which might completely break this tool.

## How to install
1. Install the module with `pip`
`pip install cson-to-markdown`

## How to use

### CLI
There's 3 arguments that can be provided;

1. The folder with the `.cson` files that need to be converted (looks recursive  in this path for all compatible files).
1. **Optional** target folder for markdown file output. If no value is provided, they will be stored in the same folder as the `.cson` files.
1. **Optional** folder containing the `boostnote.json` file. This contains the key-name pairs of the folders defined in the Boostnote aplication itself.

```bash
python -m cson_to_markdown ~/my/folder/with/cson/files ~/target/folder/optional
```

### Python:
```python
from cson_to_markdown import FileConverter


converter = FileConverter("folder/with/cson", "optional/target/folder", "optional/boostnote/settings/dir")
converter.convert()
```

## How to configure
There are a few settings that can be configured through environment variables, defined in `cson_to_markdown/config.py`.
We will by default first look at an appropriately named environemnt variable, and fall back to the defaults if none were found.

These are the current settings, which work for the Boostnote use-case specifically.
```python
    _config = {
        "MARKDOWN_START": "content: '''",
        "MARKDOWN_END": "'''",
        "TITLE_INDICATOR": 'title: "',
        "FOLDER_INDICATOR": 'folder: "',
        "YAML_STRING_INDICATOR": '"',
        "CSON_EXTENSION": ".cson",
        "MARKDOWN_EXTENSION": ".md",
        "METADATA_EXTENSION": ".yml",
        "METADATA_FOLDER": "meta",
        "BNOTE_SETTINGS_FILE": "boostnote.json",
    }
```

To overwrite, simply set a new environment variable in your terminal, or add it to your `.bashrc` file:
`export MARKDOWN_START="new start delimiter"`
