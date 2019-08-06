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
    NEUTRAL = auto()
    COLD = auto()
    HOT = auto()
