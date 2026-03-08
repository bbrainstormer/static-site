import unittest

from parser import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(
            str(
                HTMLNode(
                    value="Hello",
                    children=[HTMLNode()],
                    props={"Example": "Property"},
                )
            ),
            "HTMLNode(tag=None, value='Hello', children=[HTMLNode(tag=None, value=None, children=None, props=None)], props={'Example': 'Property'})",
        )

    def test_to_props(self):
        self.assertEqual(
            HTMLNode(props={"Hi": "there", "string": "otherstring"}).props_to_html(),
            'Hi="there" string="otherstring"',
        )
