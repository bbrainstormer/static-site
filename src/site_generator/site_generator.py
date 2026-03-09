from parser import md_to_html_node, split_into_blocks


def extract_title(md: str) -> str:
    blocks = split_into_blocks(md)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No header found")


def generate_page(
    base_path: str, from_path: str, template_path: str, dest_path: str
) -> None:
    print(
        f"Generating {dest_path} from {from_path} with template {template_path} (base {base_path})"
    )
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = md_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )
    with open(dest_path, "w") as f:
        f.write(page)
