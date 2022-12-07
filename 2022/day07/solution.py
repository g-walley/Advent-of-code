
from collections import deque
import re
from typing import Deque, List, Set
from treelib import Tree, Node


class File(Node):
    """A File"""

class Folder(Node):
    """A Folder"""

class FileSystem(Tree):
    _cwd: Deque
    _re_cmd = re.compile(r"\$ (?P<name>[a-z]+)(?P<arg> .*)?")

    def __init__(self, log: str, id: str):
        super().__init__(identifier=id)
        self._cwd = deque()
        self._log_pointer = 0
        self._log = log
        self._build_from_log()
        self._update_folder_sizes()

    @property
    def cwd(self):
        if len(self._cwd) > 1:
            return self._cwd[0] + ''.join(list(self._cwd)[1:])
        else:
            return ''.join(list(self._cwd))

    def cd(self, name: str):
        if name == "..":
            self._cwd.pop()
        else:
            id = self.cwd + name  + '/'
            if not self.get_node(id):
                self.add_node(
                    Folder(name, id, data={"depth": len(self.cwd)}),
                    parent=self.cwd if self.cwd != '' else None
                )
            self._cwd.append(name + '/')
        self._log_pointer += 1

    def ls(self):
        self._log_pointer += 1
        re_file = re.compile(r"^(?P<size>\d+) (?P<name>.*)")
        while not self._re_cmd.match(self._log[self._log_pointer]):
            line = self._log[self._log_pointer]
            file = re_file.match(line)
            if file:
                file_details = file.groupdict()
                self.add_node(
                    File(
                        tag=file_details["name"],
                        identifier=self.cwd + file_details["name"],
                        data={
                            "size": int(file_details["size"]),
                            "depth": len(self.cwd),
                        }
                    ),
                    parent=self.cwd,
                )
            self._log_pointer += 1

            if self._log_pointer >= len(self._log):
                break

    def _build_from_log(self):
        self._log = self._log.splitlines()
        while self._log_pointer < len(self._log):
            cmd = self._re_cmd.match(self._log[self._log_pointer])
            if cmd:
                cmd_dict = cmd.groupdict()
                if cmd_dict["name"] == "cd":
                    self.cd(cmd_dict["arg"].strip())
                elif cmd_dict["name"] == "ls":
                    self.ls()
            else:
                assert False, "Didn't find a command"

    def _update_folder_sizes(self):
        for node in self.nodes.values():
            if isinstance(node, Folder):
                node.data["size"] = 0
        nodes: List[Node] = sorted(list(self.nodes.values()), key=lambda x: x.data["depth"], reverse=True)

        for node in nodes:
            folder: Folder = self.get_node(node.predecessor(self.identifier))
            if folder:
                folder.data["size"] += node.data["size"]

def pt1(raw_input):
    """part 1"""
    fs: Tree = FileSystem(log=raw_input, id="pt1")

    total = 0
    for node in fs.nodes.values():
        folder_size = node.data["size"]
        if isinstance(node, Folder) and folder_size <= 100000:
            total += folder_size

    return total

def pt2(raw_input):
    """part 2"""
    fs: Tree = FileSystem(log=raw_input, id="pt2")
    TOTAL = 70000000
    used = fs.get_node("//").data["size"]
    unused = TOTAL - used
    space_required = 30000000 - unused

    smallest_directory = TOTAL
    for node in fs.nodes.values():
        if isinstance(node, Folder):
            folder_size = node.data["size"]
            if space_required <= folder_size and folder_size < smallest_directory:
                smallest_directory = folder_size
    return smallest_directory
