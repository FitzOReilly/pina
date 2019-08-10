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

    # TODO: Document and test
    @abc.abstractmethod
    def add(self, other):
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

    def __eq__(self, other):
        equal = True

        equal &= self.heat_type == other.heat_type
        equal &= self.heat_flow == other.heat_flow
        equal &= self.supply_temperature == other.supply_temperature
        equal &= self.target_temperature == other.target_temperature
        equal &= self.temperature_difference_contribution == other.temperature_difference_contribution

        return equal
