import site_generator


def main():
    site_generator.generate_page(
        "content/index.md", "template.html", "public/index.html"
    )


if __name__ == "__main__":
    main()
