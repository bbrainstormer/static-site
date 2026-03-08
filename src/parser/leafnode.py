from typing import Dict

from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: Dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be null")
        if not self.tag:
            return self.value
        props_str = (" " + self.props_to_html()) if self.props else ""
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={repr(self.tag)}, value={repr(self.value)}, props={self.props})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LeafNode):
            return False
        return (
            self.value == other.value
            and self.tag == other.tag
            and self.props == other.props
        )
