# Cson To Markdown
Recursively scans given folder for `.cson` files, extracts the metadata and markdown,
and writes a `.md` file and a `$PATH/meta/.yml` file.
Originally intended to be used as hook for personal backups with [Boostnote](https://github.com/BoostIO/Boostnote).

**Note:** Still under development, in pre-alpha stage atm.

## How to use
Since we're using poetry instead of the entire `setup.py` config, things are still somewhat new to me.
This will definitely be updated later on.

From the CLI
```bash
python -m cson_to_markdown ~/my/folder/with/cson/files ~/target/folder/optional
```

From within the code:
```python
from cson_to_markdown import FileConverter


converter = FileConverter("folder/with/cson", "target/folder/optional")
converter.convert()
```
