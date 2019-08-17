import abc


class AbstractSegment(abc.ABC):
    """
    Abstract stream segment
    """

    def __init__(
            self,
            heat_type,
            supply_temperature,
            temperature_difference_contribution
    ):
        self._heat_type = heat_type
        self._supply_temperature = supply_temperature
        self._temperature_difference_contribution = temperature_difference_contribution

    @property
    def heat_type(self):
        return self._heat_type

    @property
    def temperature_difference_contribution(self):
        return self._temperature_difference_contribution

    @property
    def supply_temperature(self):
        return self._supply_temperature

    @property
    @abc.abstractmethod
    def target_temperature(self):
        pass

    @property
    @abc.abstractmethod
    def heat_flow(self):
        pass

    @property
    def min_temperature(self):
        if self.supply_temperature <= self.target_temperature:
            return self.supply_temperature
        else:
            return self.target_temperature

    @property
    def max_temperature(self):
        if self.supply_temperature >= self.target_temperature:
            return self.supply_temperature
        else:
            return self.target_temperature

    @abc.abstractmethod
    def shift(self, default_temperature_difference_contribution=None):
        """
        Returns the segment with supply and target temperatures shifted by
        (+ temperature_difference_contribution) for cold segments and
        (- temperature_difference_contribution) for hot segments. If the
        segment's temperature_difference_contribution is None, the
        default_temperature_difference_contribution parameter is used instead.
        If it is also None, an Exception is raised. The
        temperature_difference_contribution of the returned segment is set to 0.
        """
        pass

    @abc.abstractmethod
    def with_low_supply_temperature(self):
        """
        Returns a segment like self, but with equal supply and minimum
        temperature and equal target and maximum temperature. The supply and
        target temperatures may be swapped compared to self. The heat flow
        remains the same (its sign does not change).
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
    def add_if_possible(self, other, temperature_difference_contribution):
        """
        Returns a segment with the added heat flows of self and other if both
        have equal minimum temperature and equal maximum temperature, otherwise
        returns None.
        """
        pass

    @abc.abstractmethod
    def merge_if_possible(self, other, temperature_difference_contribution):
        """
        If self and other have equal heat capacity flow rate and one's supply
        temperature equals the other's target temperature then this method
        returns a segment with the same heat capacity flow rate and the distinct
        supply and target temperatures. Otherwise returns None.
        """
        pass

    def __eq__(self, other):
        equal = True

        equal &= self.heat_type == other.heat_type
        equal &= self.heat_flow == other.heat_flow
        equal &= self.supply_temperature == other.supply_temperature
        equal &= self.target_temperature == other.target_temperature
        equal &= self.temperature_difference_contribution == other.temperature_difference_contribution

        return equal
