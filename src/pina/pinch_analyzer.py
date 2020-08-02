from pina.heat_cascade import HeatCascade


class PinchAnalyzer:
    """
    This class performs pinch analysis calculations on a list of streams:
    heating and cooling requirements, heat cascades and the pinch
    temperature(s).
    """

    def __init__(self, default_temp_shift=None):
        self._default_temp_shift = default_temp_shift
        self._streams = []
        self._pinch_temps = []
        self._cold_utility_target = 0
        self._hot_utility_target = 0

        self._cold_cascade = HeatCascade()
        self._hot_cascade = HeatCascade()
        self._shifted_cold_cascade = HeatCascade()
        self._shifted_hot_cascade = HeatCascade()
        self._grand_cascade = HeatCascade()

    @property
    def cooling_demand(self):
        return self._hot_cascade.net_heat_flow()

    @property
    def heating_demand(self):
        return self._cold_cascade.net_heat_flow()

    @property
    def cold_utility_target(self):
        return self._cold_utility_target

    @property
    def hot_utility_target(self):
        return self._hot_utility_target

    @property
    def heat_recovery_target(self):
        return self.heating_demand - self.hot_utility_target

    @property
    def pinch_temps(self):
        return self._pinch_temps

    @property
    def default_temp_shift(self):
        return self._default_temp_shift

    @property
    def streams(self):
        return self._streams

    @property
    def cold_composite_curve(self):
        return self._cold_cascade.cumulative_heat_flow(self.cold_utility_target)

    @property
    def hot_composite_curve(self):
        return self._hot_cascade.cumulative_heat_flow()

    @property
    def shifted_cold_composite_curve(self):
        return self._shifted_cold_cascade.cumulative_heat_flow(self.cold_utility_target)

    @property
    def shifted_hot_composite_curve(self):
        return self._shifted_hot_cascade.cumulative_heat_flow()

    @property
    def grand_composite_curve(self):
        return self._grand_cascade.cumulative_heat_flow(self.cold_utility_target)

    def add_streams(self, *streams):
        """
        Adds the given streams to the stream group.
        """
        for s in streams:
            self._add_one(s)

        self._compute_targets()

    def _add_one(self, stream):
        self._streams.append(stream)

        for s in stream.cold_segments:
            self._cold_cascade.add_segments(s.with_absolute_heat_flow())
            shifted = s.shift(self.default_temp_shift)
            self._shifted_cold_cascade.add_segments(shifted.with_absolute_heat_flow())
            self._grand_cascade.add_segments(shifted.with_inverted_heat_flow())

        for s in stream.hot_segments:
            self._hot_cascade.add_segments(s.with_absolute_heat_flow())
            shifted = s.shift(self.default_temp_shift)
            self._shifted_hot_cascade.add_segments(shifted.with_absolute_heat_flow())
            self._grand_cascade.add_segments(shifted.with_inverted_heat_flow())

    def _compute_targets(self):
        heat_flows, temps = self._grand_cascade.cumulative_heat_flow()
        if heat_flows:
            min_heat_flow = min(heat_flows)
            self._pinch_temps = [
                t for t, h in zip(temps, heat_flows) if h == min_heat_flow
            ]
            self._cold_utility_target = heat_flows[0] - min_heat_flow
            self._hot_utility_target = heat_flows[-1] - min_heat_flow
        else:
            self._pinch_temps = []
            self._cold_utility_target = 0
            self._hot_utility_target = 0
