from __future__ import annotations

from datetime import datetime
from hashlib import md5
from logging import getLogger

from boto3 import Session
from botocore.config import Config
from botocore.credentials import AssumeRoleCredentialFetcher, DeferredRefreshableCredentials, JSONFileCache
from botocore.session import Session as CoreSession
from dateutil.tz import tzlocal

from botoplier.sessions import SESSION_CACHE_DIR
from botoplier.types import AwsRegion, DecoratedSession, SessionKey, Sessions
from botoplier.util.timeutils import time_usage

logger = getLogger()


def _get_user_config():
    return Config()  # XXX how about an actual user config


def _mk_create_client(base_session):
    # XXX Unused config injector, to be exposed later
    def create_client__(*args, **kwargs):
        config = _get_user_config()
        if "config" in kwargs:
            kwargs["config"] = kwargs["config"].merge(config)
        else:
            kwargs["config"] = config
        return base_session.create_client(*args, **kwargs)

    return create_client__


@time_usage(logger.debug)
def assume_role_create_session(arn: str, region: str) -> DecoratedSession:
    # Fun fact about cache usage: None of the online examples at
    # https://www.programcreek.com/python/example/112444/botocore.credentials.JSONFileCache
    # will work. This will.
    base_session = Session()._session  # pylint:disable=protected-access

    # XXX make cache optional?
    fetcher = AssumeRoleCredentialFetcher(
        client_creator=_mk_create_client(base_session),
        source_credentials=base_session.get_credentials(),
        role_arn=arn,
        cache=JSONFileCache(working_dir=SESSION_CACHE_DIR),
    )
    creds = DeferredRefreshableCredentials(method="assume-role", refresh_using=fetcher.fetch_credentials, time_fetcher=lambda: datetime.now(tzlocal()))
    botocore_session = CoreSession()
    botocore_session._credentials = creds  # pylint:disable=protected-access
    res = DecoratedSession(botocore_session=botocore_session, region_name=region)
    sts = res.client("sts", config=_get_user_config())
    caller_identity = sts.get_caller_identity()  # This call is not thread safe
    res.set_arn(caller_identity["Arn"])  # Remember the ARN using our DecoratedSession helper
    return res


def make_sessions(account_ids_by_key: dict[SessionKey, str], regions: list[AwsRegion], roles_by_key: dict[SessionKey, str]) -> Sessions:
    """Returns a list of possibly cached STS sessions.
    One session will be returned for each region-account pair of the given arguments.
    Accounts can be keyed with any string - we generally use what we call "environments".

    When passed an executor, this will submit calls to it and run authentications asynchronously.
    The function will however gather the results and never return promises.

    This could become much cleaner whenever botocore supports asyncio or anyio natively.
    """
    arns = {k: f"arn:aws:iam::{v}:{roles_by_key[k]}" for k, v in account_ids_by_key.items()}
    logger.info("Starting STS sessions (sync)...")
    sessions: dict[str, DecoratedSession] = {}
    for region in regions:
        for account_key, arn in arns.items():
            session_key = f"{region}-{account_key}"
            sessions[session_key] = assume_role_create_session(arn, region)
    return sessions


def sessions_cache_key(sessions: Sessions) -> str:
    all_sks = "|".join(sorted(sessions.keys()))
    return md5(all_sks.encode()).hexdigest()  # noqa: S324
