class HeatCascade(object):
    """
    TODO: Add documentation here
    """

    def __init__(self, segments):
        # TODO: Maybe think of a better name
        # # List of temperature-enthalpy tuples
        # self._points = []

        # Set of all temperatures, at which intervals start or end
        self._temps = set()

        # List of intervals (which are simply segments) in the cascade
        self._intervals = []

        for s in segments:
            self.add(s)

    @property
    def intervals(self):
        return self._intervals

    # TODO: Add method that returns all the temperatures with cumulative heat flows

    # TODO: Refactor this monster
    def add(self, segment):
        # self._temps.update([segment.min_temperature, segment.max_temperature])

        self._intervals = [
            new_interval
            for old_interval in self._intervals
            # for new_interval in old_interval.split(self._temps)
            for new_interval in old_interval.split([segment.min_temperature, segment.max_temperature])
        ]

        subsegments = segment.split(self._temps)

        # TODO: Extract function?
        # Add each subsegments to an existing interval if a matching one is
        # found, otherwise insert new interval
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
                    self._intervals[index] = self._intervals[index].add(s)
                    break

                index += 1
            else:
                # No matching interval found, append new one
                self._intervals.append(s)

        # TODO: HACK: Refactor this (extract function?)
        self._temps.clear()
        index = 0
        while index < len(self._intervals) - 1:
            merged_interval = self._intervals[index].merge_if_possible(self._intervals[index + 1])
            if merged_interval is not None:
                self._intervals[index] = merged_interval
                self._intervals.pop(index + 1)

            # TODO: Drop intervals with zero heat flow
            if self._intervals[index].heat_flow == 0:
                self._intervals.pop(index)
                continue

            self._temps.update([
                self._intervals[index].supply_temperature,
                self._intervals[index].target_temperature
            ])

            index += 1

        if self._intervals is not None:
            self._temps.update([
                self._intervals[-1].supply_temperature,
                self._intervals[-1].target_temperature
            ])
