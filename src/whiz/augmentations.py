from dataclasses import dataclass

from ovld import Medley

from .feature import Augment


class Augmentation(Medley):
    @classmethod
    def __class_getitem__(cls, t):
        return Augment[t, cls]


@dataclass
class Quote(Augmentation):
    # Quote from the original source supporting the value
    quote: str


@dataclass
class Justification(Augmentation):
    # Justification for this value
    justification: str


@dataclass
class Confidence(Augmentation):
    # Confidence, as a float between 0.0 (not confident at all) and 1.0 (certain)
    confidence: float


@dataclass
class Aliases(Augmentation):
    # Different names used to refer to this same thing
    aliases: list[str]


Explained = Quote + Justification + Confidence
