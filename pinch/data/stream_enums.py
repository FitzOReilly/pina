from enum import Enum, auto


class HeatType(Enum):
    """
    The possible heat types of a stream segment.
    """
    SENSIBLE = auto()
    LATENT = auto()


class StreamType(Enum):
    """
    The possible stream types.
    """
    # TODO: Should there be a NEUTRAL type?
    HOT = auto()
    COLD = auto()
