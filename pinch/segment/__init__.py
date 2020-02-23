def new(heat_flow, supply_temp, target_temp, temp_shift=None):
    """
    Creates a new segment with the given properties.
    """
    if supply_temp == target_temp:
        from pinch.segment.latent_segment import LatentSegment
        cls = LatentSegment
    else:
        from pinch.segment.sensible_segment import SensibleSegment
        cls = SensibleSegment

    return cls.new(heat_flow, supply_temp, target_temp, temp_shift)
