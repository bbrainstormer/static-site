from parser import split_into_blocks


def extract_tile(md: str) -> str:
    blocks = split_into_blocks(md)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No header found")
