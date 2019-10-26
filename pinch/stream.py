from pinch.stream_enums import StreamType


class Stream(object):
    """
    A fluid stream carrying heat. It may consist of one or more segments, each
    of which has its own properties.
    """

    def __init__(self, name, segments):
        Stream._check_segments(segments)
        self.name = name
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
    def supply_temperature(self):
        return self._segments[0].supply_temperature

    @property
    def target_temperature(self):
        return self._segments[-1].target_temperature

    @property
    def heat_flow(self):
        return sum(s.heat_flow for s in self._segments)

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
        return [s for s in self._segments if s.heat_flow == 0]

    @property
    def cold_segments(self):
        """
        Returns a list of the stream's cold segments.
        """
        return [s for s in self._segments if s.heat_flow > 0]

    @property
    def hot_segments(self):
        """
        Returns a list of the stream's hot segments.
        """
        return [s for s in self._segments if s.heat_flow < 0]

    @staticmethod
    def _check_segments(segments):
        # Do not allow an empty sequence
        if not segments:
            raise ValueError("Stream must contain at least one segment")

        # Stream must be continuous
        for i in range(len(segments) - 1):
            if (segments[i + 1].supply_temperature
                != segments[i].target_temperature):
                raise ValueError("Stream must be continuous over all segments")
