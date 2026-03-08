import re
from typing import List

from .blocks import MDBlockType, get_block_type, split_into_blocks
from .htmlnode import HTMLNode
from .nodesplitter import text_to_text_nodes
from .parentnode import ParentNode
from .textnode import TextNode
from .texttype import TextType


def md_to_html_node(md_text: str) -> HTMLNode:
    parent = ParentNode(
        "div", [get_block_html(block) for block in split_into_blocks(md_text)]
    )
    return parent


def get_block_html(block: str) -> HTMLNode:
    block_type = get_block_type(block)
    match block_type:
        case MDBlockType.PARAGRAPH:
            result = ParentNode("p", text_to_formatted_html(block))
            return result
        case MDBlockType.HEADING:
            heading_level = get_heading_level(block)
            return ParentNode(
                f"h{heading_level}", text_to_formatted_html(block[heading_level + 1 :])
            )
        case MDBlockType.QUOTE:
            return ParentNode(
                "blockquote", text_to_formatted_html(clean_quote_block(block))
            )
        case MDBlockType.CODE:
            # No internal formatting
            return ParentNode(
                "pre",
                [
                    ParentNode(
                        "code",
                        [
                            TextNode(
                                clean_code_block(block), TextType.PLAIN
                            ).to_html_node()
                        ],
                    )
                ],
            )
        case MDBlockType.ORDERED_LIST:
            return ParentNode(
                "ol",
                [
                    ParentNode("li", text_to_formatted_html(item))
                    for item in split_lists(block)
                ],
            )
        case MDBlockType.UNORDERED_LIST:
            return ParentNode(
                "ul",
                [
                    ParentNode("li", text_to_formatted_html(item))
                    for item in split_lists(block)
                ],
            )
        case _:
            raise Exception("Unimplement MDBlockType")


def get_heading_level(heading_block: str) -> int:
    match = re.match("^#?", heading_block)
    if match is None:
        return 1
    return len(match.group())


def clean_quote_block(quote_block: str) -> str:
    lines = quote_block.split("\n")
    clean_lines = [line.lstrip(">").strip() for line in lines]
    return "\n".join(clean_lines)


def clean_code_block(code_block: str) -> str:
    res = "".join(code_block.split("```")).lstrip()
    return res


def split_lists(list_block: str) -> List[str]:
    return [line.split(" ", 1)[1] for line in list_block.split("\n")]


def text_to_formatted_html(text: str) -> List[HTMLNode]:
    md_nodes = text_to_text_nodes(" ".join(text.split("\n")))
    return [node.to_html_node() for node in md_nodes]
