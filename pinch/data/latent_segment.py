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
        return self._supply_temperature

    @property
    def heat_flow(self):
        return self._heat_flow
