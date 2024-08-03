from __future__ import annotations

import re
from functools import cache
from logging import getLogger
from typing import TYPE_CHECKING

import boto3
from botocore.model import ListShape, MapShape, Shape, StructureShape
from treelib import Node, Tree

if TYPE_CHECKING:
    from botocore.client import BaseClient

logger = getLogger(__name__)


def operation_output_shape(api_name: str, operation_name: str, client: BaseClient | None = None) -> Shape:
    """Returns the output shape of any given AWS API operation.
    In botocore parlance, a shape is an object-based schema representation.

    If the client parameter is given, the api_name parameter is ignored.
    """
    if client is None:
        client = boto3.client(api_name)
    aws_operation_name = client._PY_TO_OP_NAME[operation_name]
    operation_model = client.meta.service_model.operation_model(aws_operation_name)
    return operation_model.output_shape


def _shape_tree(shape: Shape, tree: Tree, parent: Node | None = None, key: str | None = None, path: str = "", *, next_token_nodes=False):
    """Recursive core of the shape_tree() routine."""
    # Avoid creating useless NextToken nodes. This is easier than filtering
    # them out later.
    if key and key.lower() in {"nexttoken", "nextmarker"} and not next_token_nodes:
        return tree

    # First, compute a unique identifier for this node.
    # The unique identifier happens to be a valid JQ expression to pull-out
    # data of the shape (or subshape)
    if parent and isinstance(parent.data, ListShape):
        path = f"{path}[]"
    elif parent is None:
        path = " "
    else:
        path = f"{path}.{key}" if key else f"{path}.{shape.name}"

    # Second, calculate a label. This is for display _and_ search purposes.
    label = f"{key}: {shape.name} ({shape.type_name})" if key else f"{shape.name} ({shape.type_name})"

    # Create the node in tree
    node = tree.create_node(label, path, data=shape, parent=parent)

    # Depending on the specific kind of Shape we're looking at, we recurse
    # in a different way to keep building the tree.
    if isinstance(shape, StructureShape):
        for key_, sub_shape in shape.members.items():
            _shape_tree(sub_shape, tree, node, key_, path, next_token_nodes=next_token_nodes)
    elif isinstance(shape, ListShape):
        _shape_tree(shape.member, tree, node, None, path, next_token_nodes=next_token_nodes)
    elif isinstance(shape, MapShape):
        # XXX untested
        _shape_tree(shape.key, tree, node, None, path, next_token_nodes=next_token_nodes)
        _shape_tree(shape.value, tree, node, None, path, next_token_nodes=next_token_nodes)
    else:
        # We don't recuse for other shape types, like StringShape, BooleanShape
        # etc. This makes them those shape types always leaves of the tree.
        # In parsing parlance, these types behave like terminals.
        pass

    return tree


@cache
def shape_tree(shape: Shape):
    """Returns a fully expanded botocore Shape in Tree form.

    This is a convenient and powerful way to view and/or process the output
    schema of any AWS operation.
    """
    return _shape_tree(shape, Tree())


def path_to_key(shape_tree_instance, key):
    tag_re = re.compile(f"^{key}:? ")
    matching_nodes = [n for n in shape_tree_instance._nodes.values() if tag_re.search(n.tag)]
    if len(matching_nodes) == 0:
        logger.warning(f"Couldn't find a key looking like {key} in output shape")
        return None

    if len(matching_nodes) > 1:
        results = ", ".join([n.tag for n in matching_nodes])
        logger.warning(f"Ambiguous key {key}! {len(matching_nodes)} results: {results} ")
        return None

    node = matching_nodes[0]
    return node.identifier
