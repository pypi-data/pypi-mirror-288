import os.path
import shutil


def isdir(path: str) -> bool:
    return os.path.isdir(path)


def isfile(path: str) -> bool:
    return os.path.isfile(path)


def move(src, dest):
    shutil.move(src, dest)


def delete_file(path: str):
    if isfile(path):
        os.remove(path)
