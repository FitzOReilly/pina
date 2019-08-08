import unittest

from pinch.data.stream_enums import HeatType
from pinch.data.sensible_segment import SensibleSegment


class TestSensibleSegment(unittest.TestCase):
    """
    Test class for SensibleSegment
    """
    def setUp(self):
        self.cold_segment = SensibleSegment(1, 20, 200)
        self.hot_segment = SensibleSegment(1.8, 150, 50)

    def tearDown(self):
        pass

    def test_zero_temperature_difference(self):
        with self.assertRaises(ValueError):
            SensibleSegment(2, 50, 50)

    def test_heat_type(self):
        self.assertEqual(self.cold_segment.heat_type, HeatType.SENSIBLE)
        self.assertEqual(self.hot_segment.heat_type, HeatType.SENSIBLE)

    def test_heat_capacity_flowrate(self):
        self.assertEqual(self.cold_segment.heat_capacity_flowrate, 1)
        self.assertEqual(self.hot_segment.heat_capacity_flowrate, 1.8)

    def test_supply_temperature(self):
        self.assertEqual(self.cold_segment.supply_temperature, 20)
        self.assertEqual(self.hot_segment.supply_temperature, 150)

    def test_target_temperature(self):
        self.assertEqual(self.cold_segment.target_temperature, 200)
        self.assertEqual(self.hot_segment.target_temperature, 50)

    def test_heat_flow(self):
        self.assertEqual(self.cold_segment.heat_flow, 180)
        self.assertEqual(self.hot_segment.heat_flow, -180)

    def test_default_temperature_difference_contribution(self):
        self.assertEqual(self.cold_segment.temperature_difference_contribution, None)
        self.assertEqual(self.hot_segment.temperature_difference_contribution, None)

    def test_temperature_difference_contribution(self):
        segment = SensibleSegment(1, 20, 200, 5)
        self.assertEqual(segment.temperature_difference_contribution, 5)


if __name__ == "__main__":
    unittest.main()
