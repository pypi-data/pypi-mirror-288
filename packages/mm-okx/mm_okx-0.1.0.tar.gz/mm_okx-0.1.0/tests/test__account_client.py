from mm_okx.account_client import get_timestamp


def test_get_timestamp():
    res = get_timestamp()
    assert res.endswith("Z")
