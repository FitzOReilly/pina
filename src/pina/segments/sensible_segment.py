from pina.enums import HeatType
from pina.segments.base_segment import BaseSegment


class SensibleSegment(BaseSegment):
    """
    Sensible segment of a stream in which its temperature changes.
    """

    def __init__(
        self, heat_capacity_flow_rate, supply_temp, target_temp, temp_shift=None
    ):
        super().__init__(supply_temp=supply_temp, temp_shift=temp_shift)
        self._target_temp = target_temp
        self._heat_capacity_flow_rate = heat_capacity_flow_rate

    @property
    def heat_type(self):
        return HeatType.SENSIBLE

    @property
    def heat_capacity_flow_rate(self):
        return self._heat_capacity_flow_rate

    @property
    def heat_flow(self):
        return self._heat_capacity_flow_rate * (self._supply_temp - self._target_temp)

    @property
    def target_temp(self):
        return self._target_temp

    @classmethod
    def new(cls, heat_flow, supply_temp, target_temp, temp_shift=None):
        if supply_temp == target_temp:
            raise ValueError(
                "Temperatures are equal: supply_temp = {}, target_temp = {}".format(
                    supply_temp, target_temp
                )
            )

        heat_capacity_flow_rate = heat_flow / (supply_temp - target_temp)
        return cls(heat_capacity_flow_rate, supply_temp, target_temp, temp_shift)

    def clone(self):
        return SensibleSegment(
            heat_capacity_flow_rate=self.heat_capacity_flow_rate,
            supply_temp=self.supply_temp,
            target_temp=self.target_temp,
            temp_shift=self.temp_shift,
        )

    def shift(self, default_temp_shift=None):
        if self.heat_flow == 0:
            shift_by = 0
        elif self.temp_shift is not None:
            shift_by = self.temp_shift
        elif default_temp_shift is not None:
            shift_by = default_temp_shift
        else:
            raise ValueError("No temperature shift given.")

        if self.heat_flow > 0:
            shift_by *= -1

        return SensibleSegment(
            self.heat_capacity_flow_rate,
            self.supply_temp + shift_by,
            self.target_temp + shift_by,
            0,
        )

    def with_low_supply_temp(self):
        if self.supply_temp > self.target_temp:
            return SensibleSegment(
                -self.heat_capacity_flow_rate,
                self.target_temp,
                self.supply_temp,
                self.temp_shift,
            )
        else:
            return self

    def with_inverted_heat_flow(self):
        return SensibleSegment(
            -self.heat_capacity_flow_rate,
            self.supply_temp,
            self.target_temp,
            self.temp_shift,
        )

    def split(self, temperatures):
        if self.supply_temp < self.target_temp:
            return self._split_ascending(temperatures)
        elif self.supply_temp > self.target_temp:
            return self._split_descending(temperatures)
        else:
            return [self]

    def add(self, other, temp_shift=None):
        if self.heat_type != other.heat_type:
            raise ValueError(
                "Heat type mismatch: {} != {}".format(self.heat_type, other.heat_type)
            )
        elif self.min_temp != other.min_temp:
            raise ValueError(
                "Minimum temperature mismatch: {} != {}".format(
                    self.min_temp, other.min_temp
                )
            )
        elif self.max_temp != other.max_temp:
            raise ValueError(
                "Maximum temperature mismatch: {} != {}".format(
                    self.max_temp, other.max_temp
                )
            )

        if self.supply_temp == other.supply_temp:
            heat_capacity_flow_rate = (
                self.heat_capacity_flow_rate + other.heat_capacity_flow_rate
            )
        else:
            heat_capacity_flow_rate = (
                self.heat_capacity_flow_rate - other.heat_capacity_flow_rate
            )

        return SensibleSegment(
            heat_capacity_flow_rate, self.supply_temp, self.target_temp, temp_shift
        )

    def link(self, other, temp_shift=None):
        if self.heat_type != other.heat_type:
            raise ValueError(
                "Heat type mismatch: {} != {}".format(self.heat_type, other.heat_type)
            )
        elif self.heat_capacity_flow_rate != other.heat_capacity_flow_rate:
            raise ValueError(
                "Heat capacity flowrate mismatch: {} != {}".format(
                    self.heat_capacity_flow_rate, other.heat_capacity_flow_rate
                )
            )

        temp_match = False
        if self.target_temp == other.supply_temp:
            temp_match = True
            supply_temp = self.supply_temp
            target_temp = other.target_temp
        elif self.supply_temp == other.target_temp:
            temp_match = True
            supply_temp = other.supply_temp
            target_temp = self.target_temp

        if temp_match:
            return SensibleSegment(
                self.heat_capacity_flow_rate, supply_temp, target_temp, temp_shift
            )
        else:
            raise ValueError(
                "No matching supply and target temperatures found:\n"
                "\tself.supply_temp: {}, self.target_temp: {}\n"
                "\tother.supply_temp: {}, other.target_temp: {}\n".format(
                    self.supply_temp,
                    self.target_temp,
                    other.supply_temp,
                    other.target_temp,
                )
            )

    def _split_ascending(self, temperatures):
        if not temperatures:
            return [self]

        subsegments = []
        sorted_temps = sorted(temperatures)
        low_temp = self.min_temp
        high_temp = self.max_temp

        for current_temp in sorted_temps:
            if current_temp <= low_temp:
                continue

            if current_temp > high_temp:
                break

            subsegments.append(
                SensibleSegment(
                    self.heat_capacity_flow_rate,
                    low_temp,
                    current_temp,
                    self.temp_shift,
                )
            )

            low_temp = current_temp

        if low_temp < high_temp:
            subsegments.append(
                SensibleSegment(
                    self.heat_capacity_flow_rate, low_temp, high_temp, self.temp_shift
                )
            )

        return subsegments

    def _split_descending(self, temperatures):
        if not temperatures:
            return [self]

        subsegments = []
        sorted_temps = sorted(temperatures, reverse=True)
        low_temp = self.min_temp
        high_temp = self.max_temp

        for current_temp in sorted_temps:
            if current_temp >= high_temp:
                continue

            if current_temp < low_temp:
                break

            subsegments.append(
                SensibleSegment(
                    self.heat_capacity_flow_rate,
                    high_temp,
                    current_temp,
                    self.temp_shift,
                )
            )

            high_temp = current_temp

        if high_temp > low_temp:
            subsegments.append(
                SensibleSegment(
                    self.heat_capacity_flow_rate, high_temp, low_temp, self.temp_shift
                )
            )

        return subsegments

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.heat_capacity_flow_rate == other.heat_capacity_flow_rate
        )

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            type(self).__qualname__,
            self._heat_capacity_flow_rate,
            self._supply_temp,
            self._target_temp,
            self._temp_shift,
        )
