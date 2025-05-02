from serieux import deserialize, schema, serialize

from whiz.augmentations import Confidence, Quote
from whiz.feature import Augment

Q = Quote[str]
QC = Augment[str, Quote, Confidence]


def test_augment_serialization():
    data = {
        "$value": "Peter",
        "quote": "Peter was the killer",
        "confidence": 0.9,
    }
    peter = deserialize(QC, data)
    assert peter == "Peter"
    assert peter._.quote == "Peter was the killer"
    assert peter._.confidence == 0.9

    assert serialize(QC, peter) == data
    assert serialize(Q, peter) == {
        "$value": "Peter",
        "quote": "Peter was the killer",
    }


def test_augment_serialization_direct():
    thing = deserialize(QC, "HEY")
    assert thing == "HEY"
    assert serialize(QC, "HEY") == "HEY"


def test_augment_schema(data_regression):
    data_regression.check(schema(QC).compile())
