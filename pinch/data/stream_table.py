from pinch.data.heat_cascade import HeatCascade


class StreamTable(object):
    """
    Stream table that holds a number of streams and performs calculations on
    them.
    """

    def __init__(self, default_temp_diff_cont=None, streams=[]):
        self._default_temp_diff_cont = default_temp_diff_cont
        self._streams = []

        self._cold_cascade = HeatCascade()
        self._hot_cascade = HeatCascade()
        self._shifted_cold_cascade = HeatCascade()
        self._shifted_hot_cascade = HeatCascade()
        self._shifted_grand_cascade = HeatCascade()

        self.add(streams)

    @property
    def cooling_demand(self):
        return self._hot_cascade.net_heat_flow

    @property
    def heating_demand(self):
        return self._cold_cascade.net_heat_flow

    @property
    def cold_utility_target(self):
        return self._cold_utility_target

    @property
    def hot_utility_target(self):
        return self._hot_utility_target

    @property
    def heat_recovery_target(self):
        return self.cooling_demand - self._cold_utility_target

    @property
    def pinch_temps(self):
        return self._pinch_temps

    @property
    def default_temp_diff_cont(self):
        return self._default_temp_diff_cont

    @default_temp_diff_cont.setter
    def default_temp_diff_cont(self, default_temp_diff_cont):
        self._default_temp_diff_cont = default_temp_diff_cont

    @property
    def streams(self):
        return self._streams

    @property
    def cold_cascade(self):
        return self._cold_cascade

    @property
    def hot_cascade(self):
        return self._hot_cascade

    @property
    def shifted_cold_cascade(self):
        return self._shifted_cold_cascade

    @property
    def shifted_hot_cascade(self):
        return self._shifted_hot_cascade

    @property
    def shifted_grand_cascade(self):
        return self._shifted_grand_cascade

    def add(self, streams):
        """
        Adds a list of streams to the stream table.
        """
        for s in streams:
            self._add_one(s)

        self._compute_targets()

        self._cold_cascade.heat_offset = self.cold_utility_target
        self._shifted_cold_cascade.heat_offset = self.cold_utility_target
        self._shifted_grand_cascade.heat_offset = self.cold_utility_target

    def _add_one(self, stream):
        self._streams.append(stream)

        for s in stream.cold_segments:
            self._cold_cascade.add([s.with_absolute_heat_flow()])
            shifted = s.shift(self._default_temp_diff_cont)
            self._shifted_cold_cascade.add([shifted.with_absolute_heat_flow()])
            self._shifted_grand_cascade.add([shifted])

        for s in stream.hot_segments:
            self._hot_cascade.add([s.with_absolute_heat_flow()])
            shifted = s.shift(self._default_temp_diff_cont)
            self._shifted_hot_cascade.add([shifted.with_absolute_heat_flow()])
            self._shifted_grand_cascade.add([shifted])

    def _compute_targets(self):
        temps, heat_flows = \
            self._shifted_grand_cascade.cumulative_heat_flow
        if heat_flows:
            min_heat_flow = min(heat_flows)
            self._pinch_temps = [
                t for t, h in zip(temps, heat_flows) if h == min_heat_flow]
            self._cold_utility_target = heat_flows[0] - min_heat_flow
            self._hot_utility_target = heat_flows[-1] - min_heat_flow
        else:
            self._pinch_temps = []
            self._cold_utility_target = 0
            self._hot_utility_target = 0
