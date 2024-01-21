import frontmatter

from markdown2anki.utils import common_types as Types


class MarkdownHandler:
    def __init__(self, path: Types.PathString) -> None:
        self.filepath = path
        self._PostObject = frontmatter.load(path)
        self.content = self._PostObject.content
        self.metadata = self._PostObject.metadata

    def get_frontmatter_text(self):
        yaml_text = frontmatter.YAMLHandler().export(self.metadata)
        frontmatter_text = "---\n" + yaml_text + "\n---\n\n"
        return frontmatter_text
