from pinch.data.abstract_segment import AbstractSegment
from pinch.data.stream_enums import HeatType


class SensibleSegment(AbstractSegment):
    """
    Sensible segment of a stream in which its temperature changes.
    """
    def __init__(
            self,
            heat_capacity_flow_rate,
            supply_temperature,
            target_temperature,
            temperature_difference_contribution=None
    ):
        super().__init__(
            heat_type=HeatType.SENSIBLE,
            supply_temperature=supply_temperature,
            temperature_difference_contribution=temperature_difference_contribution
        )
        self._target_temperature = target_temperature
        self._heat_capacity_flow_rate = heat_capacity_flow_rate

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def heat_capacity_flowrate(self):
        return self._heat_capacity_flow_rate

    @property
    def heat_flow(self):
        return \
            self._heat_capacity_flow_rate \
            * (self._target_temperature - self._supply_temperature)
