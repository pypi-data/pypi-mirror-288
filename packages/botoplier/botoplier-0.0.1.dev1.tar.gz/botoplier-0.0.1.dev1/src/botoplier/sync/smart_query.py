from __future__ import annotations

from collections.abc import Iterable
from functools import cache
from logging import getLogger
from typing import TYPE_CHECKING

import jq

from botoplier import _shapes
from botoplier.util import json, listutils, treeutils

if TYPE_CHECKING:
    from boto3 import Session
    from botocore.client import BaseClient

logger = getLogger(__name__)


def pages_of(client, paginator_name, **kwargs):
    paginator = client.get_paginator(paginator_name)
    # XXX Default configuration from schema/settings?
    page_size = kwargs.pop("PageSize", 100)
    page_iterator = paginator.paginate(PaginationConfig=dict(PageSize=page_size), **kwargs)
    yield from page_iterator


@cache
def jq_compile(jq_expression):
    logger.debug(f"Compiling JQ expression: '{jq_expression}'")
    return jq.compile(jq_expression)


def unnest(things, shape, subtree_key) -> Iterable[dict | str]:
    tree = _shapes.shape_tree(shape)

    # Figure out which subtree to unnest from
    if subtree_key is None:
        node = treeutils.first_branching_node(tree)
        path = node.identifier if node else None
    else:
        path = _shapes.path_to_key(tree, subtree_key)

    # Compute the path expression if possible
    if path is None or path == " ":
        path = "."

    # XXX port this logic to JMESPath, that comes bundled with botocore and will remove a dependency
    jqe = jq_compile(path)

    # Really a shame we have to dump/parse an extra time.
    # It's a price I'm willing to pay to avoid implementing a jq subset.
    stringified_things = json.dumps(things)
    return jqe.input(text=stringified_things).all()


def unnest_single_thing(things):
    if isinstance(things, list):
        if len(things) == 0:
            return None
        if len(things) == 1:
            return things[0]
        err_msg = f"The single option is set but result has {len(things)} records."
        raise RuntimeError(err_msg)
    err_msg = f"The single option is set, which is meaningless for results of type '{type(things)}'."
    raise TypeError(err_msg)


def _smart_query(client: BaseClient, operation: str, *, pagination=None, subtree=None, single=None, **kwargs):
    shape = _shapes.operation_output_shape("", operation, client)
    service_name = client.meta._service_model.service_name
    pretty_args = ", ".join([f"{k}={v}" for k, v in kwargs.items()])

    # XXX when pagination is None, we may be able to determine if we have to turn it off even
    #     when client.can_paginate(operation).
    #
    #     Sample exception:
    #     An error occurred (InvalidParameterCombination) when calling the DescribeInstanceStatus
    #     operation: The parameter instanceIdsSet cannot be used with the parameter maxResults

    # XXX ensure that operation resolves to a GET op ... maybe
    if (pagination is None and client.can_paginate(operation)) or pagination:
        logger.debug(f"{service_name}.{operation}({pretty_args}) [paginated]")
        pages = pages_of(client, operation, **kwargs)
        result = [unnest(p, shape, subtree) for p in pages]
        result = listutils.flatten(result)
    else:
        logger.debug(f"{service_name}.{operation}({pretty_args}) [direct]")
        method = getattr(client, operation)
        result = method(**kwargs)
        result = unnest(result, shape, subtree)

    return unnest_single_thing(result) if single else result


# XXX provide proper typing for args by relying on boto3-stubs
def smart_query(
    session: Session, api: str, operation: str, *, pagination: bool | None = None, subtree: str | None = None, single: bool | None = None, **kwargs
):
    """This function provides a one-stop shop abstraction for every AWS API call.
    It provides a large amount of utility - you don't always need to use it all.

    The session and api parameters are the most important. For instance
    `smart_query("ec2", "describe_instances")`. See the boto3 documentation for full
    reference on all supported calls and their parameters.

    Pass any specific arguments to the AWS API operation as keyword arguments. For
    instance: `smart_query("ec2", "describe-images", ImageIds=["amiXXX"])`.

    Parameters:
        pagination (bool): When left at None, its default value, smart_query autodetects
        if the operation can be paginated, and automatically does pagination and unnesting.
        When set to False forces the non-paginating way, which is required for some API calls
        in conjunction with some arguments.

        subtree (str): Controls automatic un-nesting. By default, smart query locates the first
        interesting levels in the tree returned by the API. You might be more interested in
        sub-trees. Instead of writing repetitive, error prone mappers everytime, you may just
        specify a key name and smart_query will pull the right subtree for you.

        single (bool): Controls extra un-nesting. Most calls return lists of things. If
        you are sure that the call will return zero or one thing, setting single=True will
        un-nest the argument from the result value. However, if more than one thing is returned,
        it will raise an error.
    """
    client = session.client(api, region_name=session.region_name)
    return _smart_query(client, operation, pagination=pagination, subtree=subtree, single=single, **kwargs)
