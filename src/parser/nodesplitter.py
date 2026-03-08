import re
from typing import Dict, List, Tuple

from .textnode import TextNode
from .texttype import TextType

TEXT_TYPE_DELIMITERS: Dict[str, TextType] = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def text_to_text_nodes(text: str) -> List[TextNode]:
    nodes: List[TextNode] = [TextNode(text, TextType.PLAIN)]
    for delimiter, text_type in TEXT_TYPE_DELIMITERS.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [node for node in nodes if node.text]


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, new_text_type: TextType
) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        # Even number of segments means an odd number of delimiters
        # Which means something's unmatched
        if len(sections) % 2 == 0:
            raise Exception(str(sections))
        # Each delimiter swaps between being inside and outside
        new_nodes.extend(
            (
                TextNode(
                    section, TextType.PLAIN if (i % 2 == 0) else new_text_type, None
                )
                for i, section in enumerate(sections)
                if section != ""
            )
        )
    return new_nodes


def split_nodes_image(nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in nodes:
        text = node.text
        images = extract_markdown_images(text)
        if images == []:
            new_nodes.append(node)
            continue
        for alt, link in images:
            prev_text, text = text.split(f"![{alt}]({link})", 1)
            if prev_text:
                new_nodes.append(TextNode(prev_text, node.text_type))
            new_nodes.append(TextNode(alt, TextType.IMG, link))
        if text:
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes


def split_nodes_link(nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in nodes:
        text = node.text
        links = extract_markdown_links(text)
        if links == []:
            new_nodes.append(node)
            continue
        for link_text, url in links:
            prev_text, text = text.split(f"[{link_text}]({url})", 1)
            if prev_text:
                new_nodes.append(TextNode(prev_text, node.text_type))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
        if text:
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes


def extract_markdown_images(md_text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", md_text)


def extract_markdown_links(md_text: str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", md_text)
