from pinch.segments.base_segment import BaseSegment
from pinch.stream_enums import HeatType


class LatentSegment(BaseSegment):
    """
    Latent segment of a stream in which its temperature does not change.
    """

    def __init__(self, heat_flow, supply_temp, temp_diff_contrib=None):
        super().__init__(
            supply_temp=supply_temp,
            temp_diff_contrib=temp_diff_contrib
        )
        self._heat_flow = heat_flow

    @property
    def heat_type(self):
        return HeatType.LATENT

    @property
    def target_temp(self):
        # Supply and target temperatures are equal in a latent segment
        return self._supply_temp

    @property
    def heat_flow(self):
        return self._heat_flow

    def shift(self, default_temp_diff_contrib=None):
        shift_by = None

        if self.heat_flow == 0:
            shift_by = 0

        if shift_by is None:
            shift_by = self.temp_diff_contrib
            if shift_by is None:
                shift_by = default_temp_diff_contrib
                if shift_by is None:
                    raise ValueError("No temperature difference contribution given.")

        if self.heat_flow < 0:
            shift_by *= -1

        return LatentSegment(
            self._heat_flow, self._supply_temp + shift_by, 0)

    def with_low_supply_temp(self):
        return self

    def with_inverted_heat_flow(self):
        return \
            LatentSegment(
                - self._heat_flow,
                self._supply_temp,
                self._temp_diff_contrib
            )

    def split(self, temperatures):
        # There is nothing to split in a latent segment because it has a
        # temperature range of 0, so the returned list always contains the
        # entire segment
        return [self]

    def add(self, other, temp_diff_contrib=None):
        if self.heat_type != other.heat_type:
            raise ValueError("Heat type mismatch: {} != {}".format(
                self.heat_type, other.heat_type))
        elif self._supply_temp != other.supply_temp:
            raise ValueError("Temperature mismatch: {} != {}".format(
                self._supply_temp, other.supply_temp))

        return LatentSegment(
            self._heat_flow + other.heat_flow,
            self._supply_temp,
            temp_diff_contrib
        )

    def link(self, other, temp_diff_contrib=None):
        return self.add(other, temp_diff_contrib)

    def __repr__(self):
        return \
            "{}({}, {}, {})".format(
                type(self).__qualname__,
                self._heat_flow,
                self._supply_temp,
                self._temp_diff_contrib
            )
