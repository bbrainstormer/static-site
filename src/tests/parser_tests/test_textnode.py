import unittest

from parser import LeafNode, TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("New text node", TextType.BOLD, None)
        node2 = TextNode("New text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        self.assertEqual(str(node), 'TextNode("New text node", TextType.BOLD, None)')

    def test_convert(self):
        node = TextNode("Plaintext", TextType.PLAIN, None)
        node_b = TextNode("Bold", TextType.BOLD, None)
        node_i = TextNode("Italic", TextType.ITALIC, None)
        node_c = TextNode("Code", TextType.CODE, None)
        node_img = TextNode(
            "Flower",
            TextType.IMG,
            "https://images.pexels.com/photos/1214259/pexels-photo-1214259.jpeg",
        )
        node_url = TextNode("Search engine", TextType.LINK, "google.com")
        self.assertEqual(
            [
                n.to_html_node()
                for n in [node, node_b, node_i, node_c, node_img, node_url]
            ],
            [
                LeafNode(None, "Plaintext", None),
                LeafNode("b", "Bold", None),
                LeafNode("i", "Italic", None),
                LeafNode("code", "Code", None),
                LeafNode(
                    "img",
                    "",
                    {
                        "src": "https://images.pexels.com/photos/1214259/pexels-photo-1214259.jpeg",
                        "alt": "Flower",
                    },
                ),
                LeafNode("a", "Search engine", {"href": "google.com"}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
