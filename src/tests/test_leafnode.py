import unittest

from parser import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_properties(self):
        node = LeafNode("h1", "header", {"style": "color:red"})
        self.assertEqual(node.to_html(), '<h1 style="color:red">header</h1>')

    def test_no_value(self):
        node = LeafNode("img", None)  # pyright: ignore[reportArgumentType]
        self.assertRaises(ValueError, node.to_html)

    def test_repr(self):
        node = LeafNode("t", "value", {})
        self.assertEqual(str(node), "LeafNode(tag='t', value='value', props={})")

    def test_to_html_blank(self):
        node = LeafNode(None, "The fitnessgram pacer test is")
        self.assertEqual(node.to_html(), "The fitnessgram pacer test is")
