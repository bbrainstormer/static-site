import unittest

from parser import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)


class TestNodeSplitter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual([], split_nodes_delimiter([], "`", TextType.LINK))

    def simple_test(self):
        self.assertEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
            split_nodes_delimiter(
                [TextNode("This is **bold** text", TextType.PLAIN)], "**", TextType.BOLD
            ),
        )

    def test_missing_delimiter(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [TextNode("**bold", TextType.PLAIN)],
                "**",
                TextType.BOLD,
            )

    def test_no_empty(self):
        self.assertEqual(
            [TextNode("a", TextType.PLAIN), TextNode("b", TextType.BOLD)],
            split_nodes_delimiter(
                [TextNode("a**b**", TextType.PLAIN)], "**", TextType.BOLD
            ),
        )

    def test_multiple(self):
        split = split_nodes_delimiter(
            [TextNode("Test _>1_ splits _made_", TextType.PLAIN)],
            "_",
            TextType.ITALIC,
        )
        self.assertEqual(
            [
                TextNode("Test ", TextType.PLAIN),
                TextNode(">1", TextType.ITALIC),
                TextNode(" splits ", TextType.PLAIN),
                TextNode("made", TextType.ITALIC),
            ],
            split,
        )

    def test_not_plain(self):
        self.assertEqual(
            [
                TextNode("The ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" block ", TextType.PLAIN),
                TextNode("works", TextType.ITALIC),
                TextNode(".", TextType.PLAIN),
            ],
            split_nodes_delimiter(
                [
                    TextNode("The `code`", TextType.PLAIN),
                    TextNode(" block ", TextType.PLAIN),
                    TextNode("works", TextType.ITALIC),
                    TextNode(".", TextType.PLAIN),
                ],
                "`",
                TextType.CODE,
            ),
        )

    def text_split_links(self):
        self.assertEqual(
            split_nodes_link([TextNode("Go (here)[virus.com]", TextType.PLAIN)]),
            [
                TextNode("Go ", TextType.PLAIN),
                TextNode("here", TextType.LINK, "virus.com"),
            ],
        )

    def test_split_images(self):
        self.assertEqual(
            split_nodes_image([TextNode("![alt](link)", TextType.PLAIN)]),
            [TextNode("alt", TextType.IMG, "link")],
        )

    def test_img_extraction(self):
        self.assertEqual(
            extract_markdown_images(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            ),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_link_extraction(self):
        self.assertEqual(
            extract_markdown_links(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            ),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_parse_empty(self):
        self.assertEqual(text_to_text_nodes(""), [])

    def test_parsing(self):
        self.assertEqual(
            text_to_text_nodes(
                "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            ),
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode(
                    "obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )
