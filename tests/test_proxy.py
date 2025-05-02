from serieux import serialize

from whiz.proxy import AugmentedProxy


def test_proxy_serialization():
    prox = AugmentedProxy("hello", {})
    assert serialize(str, prox) == "hello"


def test_proxy_repr():
    prox = AugmentedProxy("hello", {})
    assert repr(prox) == "<'hello'>"
