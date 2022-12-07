
from collections import deque
import re
from typing import Deque, Dict, Set, Union


class File():
    name: str
    _size: int

    def __init__(self, name: str, size: Union[int, str]):
        self.name = name
        self._size = size

    @property
    def size(self) -> int:
        return self._size


class FileSystem():
    _fs: Dict
    _cwd: Deque
    _re_cmd = re.compile(r"\$ (?P<name>[a-z]+)(?P<arg> .*)?")

    def __init__(self, log: str):
        self._folders = {}
        self._cwd = deque()
        self._log_pointer = 0
        self._log = log
        self._build_from_log()
        self._calc_folder_sizes()

    @property
    def cwd(self):
        return list(self._cwd)

    def ls(self):
        self._log_pointer += 1
        re_file = re.compile(r"^(?P<size>\d+) (?P<name>.*)")
        while not self._re_cmd.match(self._log[self._log_pointer]):
            f = re_file.match(self._log[self._log_pointer])
            if f:
                gd = f.groupdict()
                self._folders[self.mk_fn(gd["name"])] = gd["size"]
            self._log_pointer += 1

            if self._log_pointer >= len(self._log):
                break

    def mk_fn(self, name: str):
        return tuple(self.cwd + [name])

    def cd(self, cmd: str):
        if cmd == "..":
            self._cwd.pop()
        else:
            self._folders[self.mk_fn(cmd)] = 'dir'
            self._cwd.append(cmd)
        self._log_pointer += 1

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

    def _calc_folder_sizes(self):
        directories = {k for k, v in self._folders.items() if v == 'dir'}
        print(directories)


def pt1(raw_input):
    """part 1"""
    fs = FileSystem(log=raw_input)
    print(fs._folders)

def pt2(raw_input):
    """part 2"""