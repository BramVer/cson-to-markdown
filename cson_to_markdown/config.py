from smart_getenv import getenv


class Config:
    _config = {
        "MARKDOWN_START": "content: '''",
        "MARKDOWN_END": "'''",
        "TITLE_INDICATOR": 'title: "',
        "TITLE_END_CHAR": '"',
        "CSON_EXTENSION": ".cson",
        "MARKDOWN_EXTENSION": ".md",
        "METADATA_EXTENSION": ".yml",
        "METADATA_SUB_FOLDER": "meta",
    }

    def get(self, key, _type=None):
        kwargs = {"name": key, "default": self._config.get(key)}

        if _type:
            kwargs["type"] = _type

        return getenv(**kwargs)
