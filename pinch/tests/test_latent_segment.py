import unittest

from pinch.data.latent_segment import LatentSegment
from pinch.data.sensible_segment import SensibleSegment
from pinch.data.stream_enums import HeatType


class TestLatentSegment(unittest.TestCase):
    """
    Test class for LatentSegment
    """
    def setUp(self):
        self.cold_segment = LatentSegment(200, 100)
        self.hot_segment = LatentSegment(-300, 150)

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
        self.assertEqual(self.cold_segment.temperature_difference_contribution, None)
        self.assertEqual(self.hot_segment.temperature_difference_contribution, None)

    def test_temperature_difference_contribution(self):
        segment = LatentSegment(100, 200, 10)
        self.assertEqual(segment.temperature_difference_contribution, 10)

    def test_min_and_max_temperatures(self):
        self.assertEqual(self.cold_segment.min_temperature, 100)
        self.assertEqual(self.cold_segment.max_temperature, 100)
        self.assertEqual(self.hot_segment.min_temperature, 150)
        self.assertEqual(self.hot_segment.max_temperature, 150)

    def test_split(self):
        segment_temp_included = [100, 150]
        segment_temp_not_included = [90, 140]
        self.assertEqual(self.cold_segment.split([]), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(segment_temp_included), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(segment_temp_not_included), [self.cold_segment])

        self.assertEqual(self.hot_segment.split([]), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(segment_temp_included), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(segment_temp_not_included), [self.hot_segment])

    def test_equality_comparison(self):
        self.assertEqual(self.cold_segment, LatentSegment(200, 100))
        self.assertNotEqual(self.cold_segment, LatentSegment(200, 100, 10))
        self.assertNotEqual(self.cold_segment, LatentSegment(300, 100))
        self.assertNotEqual(self.cold_segment, LatentSegment(200, 150))
        self.assertNotEqual(self.cold_segment, SensibleSegment(4, 100, 150))

        self.assertEqual(self.hot_segment, LatentSegment(-300, 150))
        self.assertNotEqual(self.hot_segment, LatentSegment(-300, 150, 5))
        self.assertNotEqual(self.hot_segment, LatentSegment(-200, 150))
        self.assertNotEqual(self.hot_segment, LatentSegment(-300, 240))
        self.assertNotEqual(self.cold_segment, SensibleSegment(6, 150, 100))


if __name__ == "__main__":
    unittest.main()
