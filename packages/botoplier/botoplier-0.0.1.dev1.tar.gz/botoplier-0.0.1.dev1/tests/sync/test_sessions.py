from botoplier.sync.sessions import make_sessions
from moto import mock_aws


@mock_aws
def test_basic():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    assert "eu-west-3-testA" in sessions
    assert len(sessions) == 1


@mock_aws
def test_multi_region():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3", "eu-north-1"], {"testA": "myroles/test"})
    assert "eu-west-3-testA" in sessions
    assert "eu-north-1-testA" in sessions
    assert len(sessions) == 2
