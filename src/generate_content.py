import os
import shutil

import site_generator


def cp_folder(path: str, new_path: str) -> None:
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    os.mkdir(new_path)
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            shutil.copy(os.path.join(path, item), new_path)
        else:
            cp_folder(os.path.join(path, item), os.path.join(new_path, item))


def generate_pages_recursive(
    content_path: str, template_path: str, dest_dir_path: str
) -> None:
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.scandir(content_path):
        if item.is_dir():
            generate_pages_recursive(
                item.path, template_path, os.path.join(dest_dir_path, item.name)
            )
        elif item.name.endswith(".md"):
            html_name = os.path.splitext(item.name)[0] + ".html"
            site_generator.generate_page(
                item.path, template_path, os.path.join(dest_dir_path, html_name)
            )


def main():
    cp_folder("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
