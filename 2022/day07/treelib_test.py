from typing import Dict
from treelib import Node, Tree

class FolderContents():
    files: Dict[str, int] = {}

    @property
    def size(self):
        return sum([v.get["size"] for v in self.files.values()])


t = Tree(identifier="fs")

t.add_node(Node('/', '/', data=FolderContents()))
t.add_node(Node('a', 'abc', data=FolderContents()), parent='/')
t.add_node(Node('a', 'def', data=FolderContents()), parent='abc')

n: Node = t.get_node('def')
d: FolderContents = n.data
d.files["c.txt"] = 2512
print(n)
print(n.data.files)
print(t)

print(n.predecessor("fs"))
# for nodes in t.nodes()