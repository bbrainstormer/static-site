from parser import TextNode, TextType


def main():
    node = TextNode("Anchor text", TextType.BOLD, None)
    print(node)


if __name__ == "__main__":
    main()
