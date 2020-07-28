def make_segment(heat_flow, supply_temp, target_temp, temp_shift=None):
    """
    Creates a new segment with the given properties.
    """
    if supply_temp == target_temp:
        from pina.segments.latent_segment import LatentSegment

        cls = LatentSegment
    else:
        from pina.segments.sensible_segment import SensibleSegment

        cls = SensibleSegment

    return cls.new(heat_flow, supply_temp, target_temp, temp_shift)
