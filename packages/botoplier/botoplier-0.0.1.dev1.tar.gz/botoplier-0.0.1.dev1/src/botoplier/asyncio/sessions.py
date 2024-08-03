from __future__ import annotations

import asyncio
from logging import getLogger
from typing import TYPE_CHECKING

from botoplier.sync.sessions import assume_role_create_session
from botoplier.util.dictutils import gather_dict

logger = getLogger()

if TYPE_CHECKING:
    from concurrent.futures import Executor, Future

    from botoplier.types import AwsRegion, DecoratedSession, SessionKey, Sessions


async def make_sessions(
    account_ids_by_key: dict[SessionKey, str], regions: list[AwsRegion], roles_by_key: dict[SessionKey, str], executor: Executor | None = None
) -> Sessions:
    """Returns a list of possibly cached STS sessions.
    One session will be returned for each region-account pair of the given arguments.
    Accounts can be keyed with any string - we generally use what we call "environments".

    When passed an executor, this will submit calls to it and run authentications asynchronously.
    The function will however gather the results and never return promises.

    This could become much cleaner whenever botocore supports asyncio or anyio natively.
    """
    arns = {k: f"arn:aws:iam::{v}:{roles_by_key[k]}" for k, v in account_ids_by_key.items()}
    loop = asyncio.get_event_loop()

    # Start assume role sessions
    logger.info("Starting STS sessions (asyncio)...")
    future_sessions: dict[str, Future[DecoratedSession]] = {}
    for region in regions:
        for account_key, arn in arns.items():
            session_key = f"{region}-{account_key}"
            future_sessions[session_key] = loop.run_in_executor(executor, assume_role_create_session, arn, region)

    # Wait for results and merge them into sessions dict. Two-liner for breakpoints.
    return await gather_dict(future_sessions)
