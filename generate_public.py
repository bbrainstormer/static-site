import os
import shutil


def cp_folder(path: str, new_path: str) -> None:
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    os.mkdir(new_path)
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            shutil.copy(os.path.join(path, item), new_path)
        else:
            cp_folder(os.path.join(path, item), os.path.join(new_path, item))


def main():
    cp_folder("static", "public")


if __name__ == "__main__":
    main()
