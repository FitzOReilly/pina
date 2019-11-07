class HeatCascade(object):
    """
    Heat cascade consisting of temperature intervals. The heat capacity flow
    rate is constant in each interval.
    """

    def __init__(self, segments=[]):
        # List of intervals (which are simply segments) in the cascade
        self._intervals = []

        # The cumulative heat flow at the lowest temperature in the cascade
        self._heat_offset = 0

        self.add(segments)

    @property
    def intervals(self):
        return self._intervals

    @property
    def heat_offset(self):
        return self._heat_offset

    @heat_offset.setter
    def heat_offset(self, heat_offset):
        self._heat_offset = heat_offset

    def add(self, segments):
        """
        Adds segments to the heat cascade, i.e. each segment's heat flow is
        added at the respective temperature range.
        """

        for s in segments:
            self._add_one(s)

    @property
    def net_heat_flow(self):
        """
        Returns the net heat flow summed over all intervals.
        """
        return sum(i.heat_flow for i in self._intervals)

    @property
    def cumulative_heat_flow(self):
        """
        Returns a tuple of two lists:
        * The first list contains the cumulative heat flows at the beginning
          and end of each interval
        * The second list contains the corresponding temperatures
        The two lists are sorted by temperature, from lowest to highest.
        The cumulative heat flow at the lowest temperature can be changed by
        setting heat_offset (default value: 0).

        The two lists form the coordinates of the composite curves.
        """
        temperatures = []
        heat_flows = []
        if self._intervals:
            temperatures.append(self._intervals[0].supply_temp)
            heat_flows.append(self._heat_offset)
            for i in self._intervals:
                if i.supply_temp != temperatures[-1]:
                    # There is a temperature gap between 2 intervals
                    temperatures.append(i.supply_temp)
                    heat_flows.append(heat_flows[-1])
                temperatures.append(i.target_temp)
                heat_flows.append(heat_flows[-1] + i.heat_flow)

        return heat_flows, temperatures

    def _add_one(self, segment):
        # Split new segment and existing intervals to get rid of overlaps
        subsegments = segment.with_low_supply_temp().split(
            temperature
            for interval in self._intervals
            for temperature in [interval.min_temp, interval.max_temp]
        )
        self._intervals = [
            new_interval
            for old_interval in self._intervals
            for new_interval in old_interval.split([
                segment.min_temp, segment.max_temp])
        ]

        self._add_tailored(subsegments)

        self._link_intervals()

    def _add_tailored(self, segments):
        # Add the segments to the heat cascade.
        #
        # The temperature range of each segment and each existing interval must
        # not overlap. They must either match exactly or be separated.
        index = 0
        for s in segments:
            while index < len(self._intervals):
                if s.min_temp >= self._intervals[index].max_temp:
                    # The segment will be added at higher temperatures
                    index += 1
                    continue

                try:
                    # Add segment to interval
                    self._intervals[index] = self._intervals[index].add(s)
                except ValueError:
                    # No matching interval found, insert new one
                    self._intervals.insert(index, s)

                break
            else:
                # No matching interval found, append new one
                self._intervals.append(s)

    def _link_intervals(self):
        # Links adjacent intervals, if possible.
        index = 0
        while index < len(self._intervals) - 1:
            try:
                self._intervals[index] = \
                    self._intervals[index].link(self._intervals[index + 1])
            except ValueError:
                pass
            else:
                self._intervals.pop(index + 1)

            if self._intervals[index].heat_flow == 0:
                self._intervals.pop(index)
                continue

            index += 1

        if self._intervals and self._intervals[-1].heat_flow == 0:
            self._intervals.pop(-1)

    def __eq__(self, other):
        equal = True

        equal &= self.intervals == other.intervals
        equal &= self.heat_offset == other.heat_offset

        return equal
