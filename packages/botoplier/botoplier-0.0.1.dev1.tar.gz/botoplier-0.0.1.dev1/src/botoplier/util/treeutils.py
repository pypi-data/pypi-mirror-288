from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treelib import Node, Tree


def first_branching_node(tree: Tree) -> Node | None:
    node = tree.root
    while node:
        children = tree.children(node)
        if len(children) == 1:
            node = children[0].identifier
        else:
            return tree.get_node(node)
    return None
