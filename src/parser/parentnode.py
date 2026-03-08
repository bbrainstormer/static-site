from typing import Dict, List

from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List[HTMLNode],
        props: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("HTMLNodes need a tag")
        elif self.children is None:
            raise ValueError("ParentNode cannot have null children")
        html_str = f"<{self.tag}"
        if self.props:
            html_str += " " + self.props_to_html()
        html_str += ">"
        html_str += "".join(child.to_html() for child in self.children)
        html_str += f"</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"ParentNode(tag={repr(self.tag)}, value={repr(self.value)}, children={self.children}, props={self.props})"
