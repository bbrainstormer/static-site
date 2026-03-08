from .htmlnode import HTMLNode
from .leafnode import LeafNode
from .texttype import TextType


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TextNode):
            print("Not text node")
            return False
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f'TextNode("{self.text}", TextType.{self.text_type.name}, {self.url})'

    def to_html_node(self) -> HTMLNode:
        match self.text_type:
            case TextType.PLAIN:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                if self.url is None:
                    raise ValueError("URL Node must have a url")
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMG:
                if self.url is None:
                    raise ValueError("Image node needs an image url")
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError("Invalid TextType")
