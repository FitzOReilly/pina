from pinch.segments.latent_segment import LatentSegment
from pinch.segments.sensible_segment import SensibleSegment


def create(heat_flow, supply_temp, target_temp, temp_diff_contrib=None):
    """
    Creates a segment. The type of segment and its parameters depend on the
    given properties.
    """

    if supply_temp == target_temp:
        return LatentSegment(heat_flow, supply_temp, temp_diff_contrib)
    else:
        return SensibleSegment(
            heat_flow / (target_temp - supply_temp),
            supply_temp,
            target_temp,
            temp_diff_contrib
        )
