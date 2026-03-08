import re
from enum import Enum
from typing import List


class MDBlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


def get_block_type(block: str) -> MDBlockType:
    if re.search(r"^#{1,6} [^\n]+$", block):
        return MDBlockType.HEADING
    elif re.search(r"^```\n[\d\D]*```$", block):
        return MDBlockType.CODE
    elif _is_quote(block):
        return MDBlockType.QUOTE
    elif _is_unordered_list(block):
        return MDBlockType.UNORDERED_LIST
    elif _is_ordered_list(block):
        return MDBlockType.ORDERED_LIST
    else:
        return MDBlockType.PARAGRAPH


def split_into_blocks(text: str) -> List[str]:
    return [block.strip() for block in text.split("\n\n") if block]


def _is_quote(block: str) -> bool:
    return all(line.startswith(">") for line in block.split("\n"))


def _is_unordered_list(block: str) -> bool:
    return all(line.startswith("- ") for line in block.split("\n"))


def _is_ordered_list(block: str) -> bool:
    return all(
        line.startswith(f"{n + 1}. ") for n, line in enumerate(block.split("\n"))
    )
