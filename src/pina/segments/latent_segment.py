from pina.enums import HeatType
from pina.segments.base_segment import BaseSegment


class LatentSegment(BaseSegment):
    """
    Latent segment of a stream in which its temperature does not change.
    """

    def __init__(self, heat_flow, supply_temp, temp_shift=None):
        super().__init__(supply_temp=supply_temp, temp_shift=temp_shift)
        self._heat_flow = heat_flow

    @property
    def heat_type(self):
        return HeatType.LATENT

    @property
    def heat_flow(self):
        return self._heat_flow

    @property
    def target_temp(self):
        # Supply and target temperatures are equal in a latent segment
        return self._supply_temp

    @classmethod
    def new(cls, heat_flow, supply_temp, target_temp, temp_shift=None):
        if supply_temp != target_temp:
            raise ValueError(
                "Temperatures are different: "
                "supply_temp = {}, target_temp = {}".format(supply_temp, target_temp)
            )

        return cls(heat_flow, supply_temp, temp_shift)

    def clone(self):
        return LatentSegment(
            heat_flow=self.heat_flow,
            supply_temp=self.supply_temp,
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

        return LatentSegment(self.heat_flow, self.supply_temp + shift_by, 0)

    def with_low_supply_temp(self):
        return self

    def with_inverted_heat_flow(self):
        return LatentSegment(-self.heat_flow, self.supply_temp, self.temp_shift)

    def split(self, temperatures):
        # There is nothing to split in a latent segment because it has a
        # temperature range of 0, so the returned list always contains the
        # entire segment
        return [self]

    def add(self, other, temp_shift=None):
        if self.heat_type != other.heat_type:
            raise ValueError(
                "Heat type mismatch: {} != {}".format(self.heat_type, other.heat_type)
            )
        elif self.supply_temp != other.supply_temp:
            raise ValueError(
                "Temperature mismatch: {} != {}".format(
                    self.supply_temp, other.supply_temp
                )
            )

        return LatentSegment(
            self.heat_flow + other.heat_flow, self.supply_temp, temp_shift
        )

    def link(self, other, temp_shift=None):
        return self.add(other, temp_shift)

    def __repr__(self):
        return "{}({}, {}, {})".format(
            type(self).__qualname__,
            self._heat_flow,
            self._supply_temp,
            self._temp_shift,
        )
