from pinch.segments.latent_segment import LatentSegment
from pinch.segments.sensible_segment import SensibleSegment


def new(heat_flow, supply_temp, target_temp, temp_diff_contrib=None):
    """
    Creates a new segment with the given properties.
    """
    if supply_temp == target_temp:
        cls = LatentSegment
    else:
        cls = SensibleSegment

    return cls.new(heat_flow, supply_temp, target_temp, temp_diff_contrib)
