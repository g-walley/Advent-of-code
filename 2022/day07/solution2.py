from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Dict, List

@dataclass
class File():
    name: str
    size: int


@dataclass
class Directory():
    name: str
    parent: Directory | None
    children: Dict[str, Directory]
    files: Dict[str, File]

    @property
    def size(self) -> int:
        return sum(child.size for child in self.children.values()) + sum(
            file.size for file in self.files.values()
        )


@dataclass
class FileSystem:
    root: Directory
    pwd: Directory
    listing: bool = False


def parse_file_system(log: List[str]) -> FileSystem:
    assert log[0] == "$ cd /"
    root_dir = Directory("root", None, {}, {})
    fs = FileSystem(root=root_dir, pwd=root_dir)

    for line in log[1:]:
        if match := re.match(r"^\$ cd(?P<arg> [A-z]+)$", line):
            child_name = match["arg"]
            if child_name not in fs.pwd.children:
                fs.pwd.children[child_name] = Directory(child_name, fs.pwd, {}, {})
            fs.pwd = fs.pwd.children[child_name]
            fs.listing = False
        elif line == "$ cd ..":
            fs.pwd = fs.pwd.parent
            fs.listing = False
        elif line == "$ cd /":
            fs.pwd = fs.root
            fs.listing = False
        elif line == "$ ls":
            fs.listing = True
        elif (match := re.match(r"^(?P<size>\d+) (?P<name>.*)$", line)) and fs.listing:
            file_name = match["name"]
            if file_name not in fs.pwd.files:
                fs.pwd.files[file_name] = File(file_name, int(match["size"]))
        elif match := re.match(r"^dir.*", line):
            # Ignoring, as cd is actually making the directory.
            ...

    return fs


def list_all_directories(root: Directory) -> list[Directory]:
    all_directories = [root]
    for child in root.children.values():
        all_directories.extend(list_all_directories(child))
    return all_directories


def pt1(log: str):
    log = [line.strip() for line in log.splitlines()]
    fs = parse_file_system(log)
    all_directories = list_all_directories(fs.root)
    return sum(directory.size for directory in all_directories if directory.size <= 100000)


def pt2(log):
    log = [line.strip() for line in log.splitlines()]
    fs = parse_file_system(log)

    all_directories = list_all_directories(fs.root)
    unused_space = 70000000 - fs.root.size
    space_needed = 30000000 - unused_space
    directory_sizes = sorted(
        [d.size for d in all_directories], key=lambda x: x
    )
    for directory_size in directory_sizes:
        if directory_size >= space_needed:
            return directory_size
    assert False