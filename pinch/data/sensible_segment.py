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
    def heat_capacity_flow_rate(self):
        return self._heat_capacity_flow_rate

    @property
    def heat_flow(self):
        return \
            self._heat_capacity_flow_rate \
            * (self._target_temperature - self._supply_temperature)

    def shift(self, default_temperature_difference_contribution=None):
        shift_by = None

        if self.heat_flow == 0:
            shift_by = 0

        if shift_by is None:
            shift_by = self.temperature_difference_contribution
            if shift_by is None:
                shift_by = default_temperature_difference_contribution
                if shift_by is None:
                    raise ValueError("No temperature difference contribution given.")

        if self.heat_flow < 0:
            shift_by *= -1

        return \
            SensibleSegment(
                self._heat_capacity_flow_rate,
                self._supply_temperature + shift_by,
                self._target_temperature + shift_by,
                0
            )

    def with_low_supply_temperature(self):
        if self.supply_temperature > self.target_temperature:
            return SensibleSegment(
                - self.heat_capacity_flow_rate,
                self.target_temperature,
                self.supply_temperature,
                self.temperature_difference_contribution
            )
        else:
            return self

    def with_inverted_heat_flow(self):
        return \
            SensibleSegment(
                - self._heat_capacity_flow_rate,
                self._supply_temperature,
                self._target_temperature,
                self._temperature_difference_contribution
            )

    def split(self, temperatures):
        if self.supply_temperature < self.target_temperature:
            return self._split_ascending(temperatures)
        elif self.supply_temperature > self.target_temperature:
            return self._split_descending(temperatures)
        else:
            return [self]

    def add_if_possible(self, other, temperature_difference_contribution=None):
        if self.heat_type == other.heat_type \
        and self.min_temperature == other.min_temperature \
        and self.max_temperature == other.max_temperature:
            if self.supply_temperature == other.supply_temperature:
                heat_capacity_flow_rate = \
                    self.heat_capacity_flow_rate + other.heat_capacity_flow_rate
            else:
                heat_capacity_flow_rate = \
                    self.heat_capacity_flow_rate - other.heat_capacity_flow_rate

            return SensibleSegment(
                heat_capacity_flow_rate,
                self._supply_temperature,
                self._target_temperature,
                temperature_difference_contribution
            )

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

    def __eq__(self, other):
        return \
            super().__eq__(other) \
            and self.heat_capacity_flow_rate == other.heat_capacity_flow_rate
