from parser import TextNode, TextType
from site_generator import utils


def main():
    node = TextNode("Anchor text", TextType.BOLD, None)
    utils.generate_page("content/index.md", "template.html", "public/index.html")
    print(node)


if __name__ == "__main__":
    main()
