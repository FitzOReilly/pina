from pinch.data.abstract_segment import AbstractSegment
from pinch.data.stream_enums import HeatType


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
            heat_type=HeatType.LATENT,
            supply_temperature=supply_temperature,
            temperature_difference_contribution=temperature_difference_contribution
        )
        self._heat_flow = heat_flow

    @property
    def target_temperature(self):
        # Supply and target temperatures are equal in a latent segment
        return self._supply_temperature

    @property
    def heat_flow(self):
        return self._heat_flow

    def with_low_supply_temperature(self):
        return self

    def split(self, temperatures):
        # There is nothing to split in a latent segment because it has a
        # temperature range of 0, so the returned list always contains the
        # entire segment
        return [self]

    def add_if_possible(self, other, temperature_difference_contribution=None):
        if self._heat_type == other.heat_type \
        and self._supply_temperature == other.supply_temperature:
            return LatentSegment(
                self._heat_flow + other.heat_flow,
                self._supply_temperature,
                temperature_difference_contribution
            )

    def merge_if_possible(self, other, temperature_difference_contribution=None):
        return self.add_if_possible(other, temperature_difference_contribution)
