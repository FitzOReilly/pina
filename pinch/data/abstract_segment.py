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

    # TODO: Rename this to return_temperature?
    @property
    @abc.abstractmethod
    def target_temperature(self):
        pass

    @property
    @abc.abstractmethod
    def heat_flow(self):
        pass
