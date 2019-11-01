from pinch.segments.abstract_segment import AbstractSegment
from pinch.stream_enums import HeatType


class LatentSegment(AbstractSegment):
    """
    Latent segment of a stream in which its temperature does not change.
    """

    def __init__(
            self,
            heat_flow,
            supply_temperature,
            temperature_difference_contribution=None
    ):
        super().__init__(
            supply_temperature=supply_temperature,
            temperature_difference_contribution=temperature_difference_contribution
        )
        self._heat_flow = heat_flow

    @property
    def heat_type(self):
        return HeatType.LATENT

    @property
    def target_temperature(self):
        # Supply and target temperatures are equal in a latent segment
        return self._supply_temperature

    @property
    def heat_flow(self):
        return self._heat_flow

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

        return LatentSegment(
            self._heat_flow, self._supply_temperature + shift_by, 0)

    def with_low_supply_temperature(self):
        return self

    def with_inverted_heat_flow(self):
        return \
            LatentSegment(
                - self._heat_flow,
                self._supply_temperature,
                self._temperature_difference_contribution
            )

    def split(self, temperatures):
        # There is nothing to split in a latent segment because it has a
        # temperature range of 0, so the returned list always contains the
        # entire segment
        return [self]

    def add(self, other, temperature_difference_contribution=None):
        if self.heat_type != other.heat_type:
            raise ValueError("Heat type mismatch: {} != {}".format(
                self.heat_type, other.heat_type))
        elif self._supply_temperature != other.supply_temperature:
            raise ValueError("Temperature mismatch: {} != {}".format(
                self._supply_temperature, other.supply_temperature))

        return LatentSegment(
            self._heat_flow + other.heat_flow,
            self._supply_temperature,
            temperature_difference_contribution
        )

    def link(self, other, temperature_difference_contribution=None):
        return self.add(other, temperature_difference_contribution)

    def __repr__(self):
        return \
            "{}({}, {}, {})".format(
                type(self).__qualname__,
                self._heat_flow,
                self._supply_temperature,
                self._temperature_difference_contribution
            )
