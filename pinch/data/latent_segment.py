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

    # TODO: Refactor + Test
    # TODO: Assert that heat types and temparatures are equal
    def add(self, other, temperature_difference_contribution=None):
        return LatentSegment(
            self._heat_flow + other.heat_flow,
            self._supply_temperature,
            temperature_difference_contribution
        )

    def split(self, temperatures):
        # There is nothing to split in a latent segment because it has a
        # temperature range of 0, so the returned list always contains the
        # entire segment
        return [self]
