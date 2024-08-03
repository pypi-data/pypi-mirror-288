# XXX provide proper typing for args by relying on boto3-stubs
import asyncio
from functools import partial

from botoplier.sync.smart_query import _smart_query


def smart_query(session, api, operation, *, executor=None, pagination=None, subtree=None, single=False, **kwargs):
    """This function provides a one-stop shop abstraction for every AWS API call.
    It provides a large amount of utility - you don't always need to use it all.

    The session and api parameters are the most important. For instance
    `smart_query("ec2", "describe_instances")`. See the boto3 documentation for full
    reference on all supported calls and their parameters.

    Pass any specific arguments to the AWS API operation as keyword arguments. For
    instance: `smart_query("ec2", "describe-images", ImageIds=["amiXXX"])`.

    Parameters:
        executor (concurrent.futures.Executor): Passing an executor makes smart_query
        behave in an asynchronous way: work will be scheduled to be ran in the executor,
        and smart query returns a Future. Not passing an executor means smart_query behaves
        synchronously: the result of the call will be returned.

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
    loop = asyncio.get_event_loop()
    closure = partial(_smart_query, client, operation, pagination=pagination, subtree=subtree, single=single, **kwargs)
    return loop.run_in_executor(executor, closure)
