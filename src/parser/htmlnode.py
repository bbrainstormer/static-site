from typing import Dict, List


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: Dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " ".join(f'{key}="{self.props[key]}"' for key in self.props)

    def __repr__(self):
        return f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, children={self.children}, props={self.props})"
