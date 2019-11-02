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

`pip install cson-to-markdown`

## How to use
### 1. CLI
I use Google's [python-fire](https://github.com/google/python-fire) to create the CLI.
You can run `cson_to_markdown --help` to get more information on the module.

There's 3 arguments that can be provided; `cson_to_markdown $arg1 $arg2 $arg3`

1. The folder with the `.cson` files that need to be converted (looks recursive  in this path for all compatible files).
1. **Optional** target folder for markdown file output. If no value is provided, they will be stored in the same folder as the `.cson` files.
1. **Optional** folder containing the `boostnote.json` file. This contains the key-name pairs of the folders defined in the Boostnote aplication itself.

```bash
# Call module directly
cson_to_markdown ~/folder/with/notes ~/output/folder ~/settings/dir

# Through python
python -m cson_to_markdown ~/folder/with/notes ~/output/folder ~/settings/dir
```

### 2. Python:
```python
from cson_to_markdown import FileConverter


converter = FileConverter("folder/with/cson", "optional/target/folder", "optional/boostnote/settings/dir")
converter.convert()
```

### 3. Git hooks
You can leverage the usefulness of git hooks, to make use of this module.
Based off of [this StackOverflow answer](https://stackoverflow.com/a/12802592/7291804), I implemented the following:
**Note:** This is not a clean way to do this, think before you copy paste this.

1. Create pre-commit hook in notes repository:
`vim .git/hooks/pre-commit`

```bash
#!/bin/bash

echo
touch .commit
exit
```

2. Create post-commit hook to create and add new files to the commit:
`vim .git/hooks/post-commit`

```bash
#!/bin/bash

cson_to_markdown $INSERT_NOTES_FOLDER $OPTIONAL_MARKDOWN_OUTPUT_FOLDER $OPTIONAL_BOOSTNOTE_SETTINGS_FOLDER

if [ -a .commit ]
    then
    rm .commit
    git add .
    git commit --amend -C HEAD --no-verify
fi
exit
```

3. Make both executable:
`chmod u+x .git/hooks/pre-commit .git/hooks/post-commit`


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
