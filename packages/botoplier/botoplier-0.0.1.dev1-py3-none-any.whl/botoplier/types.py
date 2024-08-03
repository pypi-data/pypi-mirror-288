from __future__ import annotations

from boto3 import Session
from typing_extensions import TypeAliasType

"""SessionKey strings are used everywhere as aliases to a tuple of an aws-region, and an account ARN which wraps an
aws-account-id and an aws-role.

All of botoplier operations accept a SessionKey-keyed dictionary of clients, and return SessionKey-keyed dictionaries
of results. This makes single-account/single-role code work very much the same as multi-account/multi-role code.
"""
SessionKey = TypeAliasType("SessionKey", str)

AwsRegion = TypeAliasType("AwsRegion", str)


class DecoratedSession(Session):
    """This provides more accurate string representation for Sessions.

    This string representation is then used as a caching key. One should not
    remove information from the caching key without appreciating the
    consequences.
    """

    arn: str = None
    account_id: str = None

    def set_arn(self, arn: str):
        self.arn = arn
        self.account_id = arn.split(":")[4]

    def __str__(self) -> str:
        return f"DecoratedSession(account_id={self.account_id}, region_name={self.region_name})"

    def __repr__(self) -> str:
        return self.__str__()


Sessions = dict[SessionKey, DecoratedSession]
