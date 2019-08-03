import unittest

from pinch.data.stream_enums import HeatType
from pinch.data.latent_segment import LatentSegment


class TestLatentSegment(unittest.TestCase):
    """
    Test class for LatentSegment
    """
    def setUp(self):
        self.cold_segment = LatentSegment(100, 200)
        self.hot_segment = LatentSegment(150, -300)

    def tearDown(self):
        pass

    def test_heat_type(self):
        self.assertEqual(self.cold_segment.heat_type, HeatType.LATENT)
        self.assertEqual(self.hot_segment.heat_type, HeatType.LATENT)

    def test_supply_temperature(self):
        self.assertEqual(self.cold_segment.supply_temperature, 100)
        self.assertEqual(self.hot_segment.supply_temperature, 150)

    def test_target_temperature(self):
        self.assertEqual(self.cold_segment.target_temperature, 100)
        self.assertEqual(self.hot_segment.target_temperature, 150)

    def test_heat_flow(self):
        self.assertEqual(self.cold_segment.heat_flow, 200)
        self.assertEqual(self.hot_segment.heat_flow, -300)

    def test_default_temperature_difference_contribution(self):
        self.assertEqual(self.cold_segment.temperature_difference_contribution, 0)
        self.assertEqual(self.hot_segment.temperature_difference_contribution, 0)

    def test_temperature_difference_contribution(self):
        segment = LatentSegment(100, 200, 10)
        self.assertEqual(segment.temperature_difference_contribution, 10)


if __name__ == "__main__":
    unittest.main()
