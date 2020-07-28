from enum import Enum, auto


class HeatType(Enum):
    """
    The possible heat types of a stream segment.
    """

    SENSIBLE = auto()
    LATENT = auto()
