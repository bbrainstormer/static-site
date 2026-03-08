import unittest

from parser import MDBlockType, get_block_type, split_into_blocks


class BlocksTest(unittest.TestCase):
    def test_block_split(self):
        md = """
block 1

block 2
Is two lines

- Item 1
- Item 2
"""
        self.assertEqual(
            split_into_blocks(md),
            [
                "block 1",
                "block 2\nIs two lines",
                "- Item 1\n- Item 2",
            ],
        )

    def test_gt_2_lines(self):
        md = """
        1


        2
        """
        self.assertEqual(split_into_blocks(md), ["1", "2"])

    def test_headings(self):
        blocks = [
            "# h1",
            "## h2",
            "### h3",
            "#### h4",
            "##### h5",
            "###### h6",
            "#invalid",
            "####### no h7",
        ]
        self.assertEqual(
            list(map(get_block_type, blocks)),
            [MDBlockType.HEADING] * 6 + [MDBlockType.PARAGRAPH] * 2,
        )

    def test_code_blocks(self):
        blocks = [
            "```\n```",
            "```\nprint()\n```",
            "```\nprint()\ninput()```",
            "Inline `code()` is not a block",
            "```malformed```",
        ]
        self.assertEqual(
            list(map(get_block_type, blocks)),
            [MDBlockType.CODE] * 3 + [MDBlockType.PARAGRAPH] * 2,
        )

    def test_quote_blocks(self):
        blocks = [
            "> I think therefore I am",
            "> Multiple\n> Lines",
            ">No spaces needed\n>After the bracket",
            ">Must be on\n Every line",
            "This is just a \n paragraph",
        ]
        self.assertEqual(
            list(map(get_block_type, blocks)),
            [MDBlockType.QUOTE] * 3 + [MDBlockType.PARAGRAPH] * 2,
        )

    def test_ordered_lists(self):
        blocks = [
            "\n".join(["1. one", "2. two", "3. three"]),
            "\n".join(["1. ", "2. ", "3. "]),
            "\n".join(["1", "2", "3", "4"]),
            "\n".join(["4. ", "3. ", "2. ", "1. "]),
            "\n".join(["1. "] * 3),
        ]
        self.assertEqual(
            list(map(get_block_type, blocks)),
            [MDBlockType.ORDERED_LIST] * 2 + [MDBlockType.PARAGRAPH] * 3,
        )

    def test_unordered_list(self):
        blocks = [
            "\n".join(["- Eggs", "- Mlik", "- Butter"]),
            "\n".join(["-No space", "-Incorrect"]),
            "\n".join(["* Incorrect ", "+ Items"]),
        ]

        self.assertEqual(
            list(map(get_block_type, blocks)),
            [MDBlockType.UNORDERED_LIST] + [MDBlockType.PARAGRAPH] * 2,
        )
