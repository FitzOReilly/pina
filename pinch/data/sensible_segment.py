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
        self._check_temperatures()

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def heat_capacity_flow_rate(self):
        return self._heat_capacity_flow_rate

    @property
    def heat_flow(self):
        return \
            self._heat_capacity_flow_rate \
            * (self._target_temperature - self._supply_temperature)

    # TODO: Refactor + Test
    # TODO: Rename add_if_possible? Return None if not possible
    # TODO: Assert that heat types and temparatures are equal
    def add(self, other, temperature_difference_contribution=None):
        return SensibleSegment(
            self._heat_capacity_flow_rate + other.heat_capacity_flow_rate,
            self._supply_temperature,
            self._target_temperature,
            temperature_difference_contribution
        )

    def split(self, temperatures):
        if self.heat_flow > 0:
            return self._split_ascending(temperatures)
        else:
            return self._split_descending(temperatures)

    # TODO: Clean up, document
    # TODO: Returns None, if not possible
    def merge_if_possible(self, other, temperature_difference_contribution=None):
        if self.heat_type == other.heat_type \
        and self.heat_capacity_flow_rate == other.heat_capacity_flow_rate:
            if self.target_temperature == other.supply_temperature:
                return SensibleSegment(
                    self._heat_capacity_flow_rate,
                    self._supply_temperature,
                    other.target_temperature,
                    temperature_difference_contribution
                )
            elif self.supply_temperature == other.target_temperature:
                return SensibleSegment(
                    self._heat_capacity_flow_rate,
                    other.supply_temperature,
                    self._target_temperature,
                    temperature_difference_contribution
                )

    # TODO: Allow zero heat flow?
    # If not, then such a check should be included in latent segment, too
    def _check_temperatures(self):
        if self._supply_temperature == self._target_temperature:
            raise ValueError("Supply and target temperatures must differ")

    def _split_ascending(self, temperatures):
        if not temperatures:
            return [self]

        subsegments = []
        sorted_temps = sorted(temperatures)
        low_temp = self.min_temperature
        high_temp = self.max_temperature

        for current_temp in sorted_temps:
            if current_temp <= low_temp:
                continue

            if current_temp > high_temp:
                break

            subsegments.append(SensibleSegment(
                self.heat_capacity_flow_rate,
                low_temp,
                current_temp,
                self.temperature_difference_contribution
            ))

            low_temp = current_temp

        if low_temp < high_temp:
            subsegments.append(SensibleSegment(
                self.heat_capacity_flow_rate,
                low_temp,
                high_temp,
                self.temperature_difference_contribution
            ))

        return subsegments

    def _split_descending(self, temperatures):
        if not temperatures:
            return [self]

        subsegments = []
        sorted_temps = sorted(temperatures, reverse=True)
        low_temp = self.min_temperature
        high_temp = self.max_temperature

        for current_temp in sorted_temps:
            if current_temp >= high_temp:
                continue

            if current_temp < low_temp:
                break

            subsegments.append(SensibleSegment(
                self.heat_capacity_flow_rate,
                high_temp,
                current_temp,
                self.temperature_difference_contribution
            ))

            high_temp = current_temp

        if high_temp > low_temp:
            subsegments.append(SensibleSegment(
                self.heat_capacity_flow_rate,
                high_temp,
                low_temp,
                self.temperature_difference_contribution
            ))

        return subsegments
