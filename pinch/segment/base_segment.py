import abc


class BaseSegment(abc.ABC):
    """
    Abstract base class for stream segments
    """

    def __init__(self, supply_temp, temp_diff_contrib):
        self._supply_temp = supply_temp
        self._temp_diff_contrib = temp_diff_contrib

    @property
    @abc.abstractmethod
    def heat_type(self):
        pass

    @property
    @abc.abstractmethod
    def heat_flow(self):
        pass

    @property
    def supply_temp(self):
        return self._supply_temp

    @property
    @abc.abstractmethod
    def target_temp(self):
        pass

    @property
    def temp_diff_contrib(self):
        # Temperature difference contribution
        return self._temp_diff_contrib

    @property
    def min_temp(self):
        return min(self.supply_temp, self.target_temp)

    @property
    def max_temp(self):
        return max(self.supply_temp, self.target_temp)

    @classmethod
    @abc.abstractmethod
    def new(cls, heat_flow, supply_temp, target_temp, temp_diff_contrib):
        pass

    @abc.abstractmethod
    def clone(self):
        pass

    @abc.abstractmethod
    def shift(self, default_temp_diff_contrib=None):
        """
        Returns the segment with supply and target temperatures shifted by
        (+ temp_diff_contrib) for cold segments and (- temp_diff_contrib) for
        hot segments. If the segment's temp_diff_contrib is None, the
        default_temp_diff_contrib parameter is used instead. If it is also
        None, a ValueError is raised. The temp_diff_contrib of the returned
        segment is set to 0.
        """
        pass

    @abc.abstractmethod
    def with_low_supply_temp(self):
        """
        Returns a segment like self, but with equal supply and minimum
        temperature and equal target and maximum temperature. The supply and
        target temperatures may be swapped compared to self. The heat flow
        remains the same (its sign does not change).
        """
        pass

    def with_absolute_heat_flow(self):
        """
        Returns the segment with absolute heat flow. The supply and target
        temperatures remain the same (they are not swapped).
        """
        if self.heat_flow < 0:
            return self.with_inverted_heat_flow()
        else:
            return self

    @abc.abstractmethod
    def with_inverted_heat_flow(self):
        """
        Returns the segment with inverted heat flow. The supply and target
        temperatures remain the same (they are not swapped).
        """
        pass

    @abc.abstractmethod
    def split(self, temperatures):
        """
        Splits the segment at all given temperatures and returns a list of the
        resulting subsegments. If none of the given temperatures is within the
        temperature range of the segment or temperatures is empty, the returned
        list contains the entire segment as the only element.
        """
        pass

    @abc.abstractmethod
    def add(self, other, temp_diff_contrib):
        """
        Returns a segment with the added heat flows of self and other if both
        have equal minimum temperature and equal maximum temperature, otherwise
        returns a ValueError.
        """
        pass

    @abc.abstractmethod
    def link(self, other, temp_diff_contrib):
        """
        If self and other have equal heat capacity flow rate and one's supply
        temperature equals the other's target temperature then this method
        returns a segment with the same heat capacity flow rate and the
        differing supply and target temperatures. Otherwise returns a
        ValueError.
        """
        pass

    def __eq__(self, other):
        equal = self.heat_type == other.heat_type
        equal &= self.heat_flow == other.heat_flow
        equal &= self.supply_temp == other.supply_temp
        equal &= self.target_temp == other.target_temp
        equal &= self.temp_diff_contrib == other.temp_diff_contrib

        return equal
