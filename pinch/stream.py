from pinch.stream_enums import StreamType


class Stream(object):
    """
    A fluid stream carrying heat and consisting of one or multiple segments.
    """

    def __init__(self, segments):
        """
        `segments` must meet the following conditions:
        * It must not be an empty sequence.
        * It must be continuous, i.e. there must be no temperature gaps between
          adjacent segments.
        If one of those conditions is not met, a ValueError is raised.
        """
        Stream._check_segments(segments)
        self._segments = tuple(segments)

    @property
    def stream_type(self):
        if self.heat_flow > 0:
            return StreamType.COLD
        elif self.heat_flow < 0:
            return StreamType.HOT
        else:
            return StreamType.NEUTRAL

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
        return [s for s in self.segments if s.heat_flow > 0]

    @property
    def hot_segments(self):
        """
        Returns a list of the stream's hot segments.
        """
        return [s for s in self.segments if s.heat_flow < 0]

    @staticmethod
    def _check_segments(segments):
        if not segments:
            raise ValueError("`segments` empty")

        for i in range(len(segments) - 1):
            if (segments[i].target_temp != segments[i + 1].supply_temp):
                raise ValueError(
                    "Temperature gap between adjacent segments: {}, {}"
                    .format(segments[i], segments[i + 1])
                )
