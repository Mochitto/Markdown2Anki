import frontmatter
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from markdown2anki.utils import common_types as Types


# Note: Keep MarkdownMetadata and metadata_schema in sync when changing.
class MarkdownMetadata:
    def __init__(
        self,
        deck_name: str,
        note_type_basic: str,
        note_type_cloze: str,
        tags: list[str] = [],
        no_tabs: bool = False,
    ) -> None:
        self.deck_name = deck_name
        self.note_type_basic = note_type_basic
        self.note_type_cloze = note_type_cloze
        self.tags = tags
        self.no_tabs = no_tabs


metadata_schema = {
    "type": "object",
    "properties": {
        "deck_name": {"type": "string"},
        "note_type_basic": {"type": "string"},
        "note_type_cloze": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "no_tabs": {"type": "boolean"},
    },
    "required": [
        "deck_name",
        "note_type_basic",
        "note_type_cloze",
    ],
    "optional": ["tags", "no_tabs"],
    "additionalProperties": False,
}


class MarkdownHandler:
    def __init__(self, path: Types.PathString) -> None:
        """
        From given path to markdown file create a MarkdownHandler object.

        Both content and metadata are extracted from the file and stored in the object.
        Metadata is validated against a schema.
        """
        with open(path) as f:
            self.metadata, self.content = frontmatter.parse(f.read())

        if not self.metadata:
            raise Exception("No metadata found in file.")

        try:
            validate(instance=self.metadata, schema=metadata_schema)
        except ValidationError as e:
            raise Exception(f"Invalid metadata schema: {e}")

        # Unpack unstructred metadata and pass it through the MarkdownMetadata class to
        # get the structured metadata and set defaults for optional fields, then convert
        # it back to a dict.
        self.metadata = MarkdownMetadata(**self.metadata).__dict__

        # Prepend default md2anki tag to the metadata.
        self.metadata["tags"] = ["md2anki"] + self.metadata["tags"]

    def get_frontmatter_text(self) -> str:
        """Return frontmatter text."""
        yaml_text = frontmatter.YAMLHandler().export(self.metadata)
        frontmatter_text = "---\n" + yaml_text + "\n---\n\n"
        return frontmatter_text
