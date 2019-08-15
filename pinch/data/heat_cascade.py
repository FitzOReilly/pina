class HeatCascade(object):
    """
    Heat cascade consisting of temperature intervals. The heat capacity flow
    rate is constant in each interval.
    """

    def __init__(self, segments=[]):
        # List of intervals (which are simply segments) in the cascade
        self._intervals = []

        self.add(segments)

    @property
    def intervals(self):
        return self._intervals

    def add(self, segments):
        """
        Adds segments to the heat cascade, i.e. each segment's heat flow is
        added at the respective temperature range.
        """

        for s in segments:
            self._add_one(s)

    def _add_one(self, segment):
        # Split new segment and existing intervals to get rid of overlaps
        subsegments = segment.with_low_supply_temperature().split(
            temperature
            for interval in self._intervals
            for temperature in [interval.min_temperature, interval.max_temperature]
        )
        self._intervals = [
            new_interval
            for old_interval in self._intervals
            for new_interval in old_interval.split([segment.min_temperature, segment.max_temperature])
        ]

        self._add_tailored(subsegments)

        self._merge_intervals()

    def _add_tailored(self, subsegments):
        # Add the subsegments to the heat cascade.
        #
        # The temperature range of each subsegment and each existing interval
        # must not overlap. They must either match exactly or be separated.
        index = 0
        for s in subsegments:
            while index < len(self._intervals):
                if s.min_temperature < self._intervals[index].min_temperature:
                    # No matching interval found, insert new one
                    self._intervals.insert(index, s)
                    break
                elif s.min_temperature == self._intervals[index].min_temperature \
                and s.max_temperature == self._intervals[index].max_temperature:
                    # Matching interval found, add segment to it
                    self._intervals[index] = self._intervals[index].add_if_possible(s)
                    break

                index += 1
            else:
                # No matching interval found, append new one
                self._intervals.append(s)

    def _merge_intervals(self):
        # Merges adjacent intervals, if possible.
        index = 0
        while index < len(self._intervals) - 1:
            merged_interval = self._intervals[index].merge_if_possible(self._intervals[index + 1])
            if merged_interval is not None:
                self._intervals[index] = merged_interval
                self._intervals.pop(index + 1)

            if self._intervals[index].heat_flow == 0:
                self._intervals.pop(index)
                continue

            index += 1

        if self._intervals and self._intervals[-1].heat_flow == 0:
            self._intervals.pop(-1)
