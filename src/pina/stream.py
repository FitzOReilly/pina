class Stream:
    """
    A fluid stream carrying heat and consisting of one or multiple segments.
    """

    def __init__(self, *segments):
        """
        `segments` must meet the following conditions:
        * It must not be an empty sequence.
        * It must be continuous, i.e. there must be no temperature gaps between
          adjacent segments.
        If one of those conditions is not met, a ValueError is raised.
        """
        Stream._check_segments(segments)
        self._segments = segments

    @property
    def heat_flow(self):
        return sum(s.heat_flow for s in self.segments)

    @property
    def supply_temp(self):
        return self.segments[0].supply_temp

    @property
    def target_temp(self):
        return self.segments[-1].target_temp

    @property
    def segments(self):
        """
        Returns a list of the stream's segments.
        """
        return list(self._segments)

    @property
    def neutral_segments(self):
        """
        Returns a list of the stream's neutral segments.
        """
        return [s for s in self.segments if s.heat_flow == 0]

    @property
    def cold_segments(self):
        """
        Returns a list of the stream's cold segments.
        """
        return [s for s in self.segments if s.heat_flow < 0]

    @property
    def hot_segments(self):
        """
        Returns a list of the stream's hot segments.
        """
        return [s for s in self.segments if s.heat_flow > 0]

    @staticmethod
    def _check_segments(segments):
        if not segments:
            raise ValueError("`segments` empty")

        prev = None
        for current in segments:
            if prev is not None and current.supply_temp != prev.target_temp:
                raise ValueError(
                    "Temperature gap between adjacent segments: {}, {}".format(
                        prev, current
                    )
                )

            prev = current

    def __eq__(self, other):
        return self.segments == other.segments

    def __repr__(self):
        return "{}{}".format(type(self).__qualname__, self._segments)


def make_stream(heat_flow, supply_temp, target_temp, temp_shift=None):
    """
    Convenience function to create a single segment stream.
    """
    return make_segmented_stream([heat_flow, supply_temp, target_temp, temp_shift])


def make_segmented_stream(*segments):
    """
    Convenience function to create a segmented stream. Each argument represents
    one segment. It must have the following form:
    [heat_flow, supply_temp, target_temp, temp_shift=None]
    """
    from pina.segments import make_segment

    return Stream(*(make_segment(*s) for s in segments))
