import unittest

from site_generator import utils


class TestExtractTile(unittest.TestCase):
    def test_no_title(self):
        with self.assertRaises(ValueError):
            utils.extract_title("## No header")

    def test_extract_title(self):
        self.assertEqual(
            utils.extract_title("# Using calculus to get laid"),
            "Using calculus to get laid",
        )

    def test_not_first_block(self):
        self.assertEqual(
            utils.extract_title(
                """Here's some example text

# Title"""
            ),
            "Title",
        )
