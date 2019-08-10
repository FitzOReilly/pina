import unittest

from pinch.data.latent_segment import LatentSegment
from pinch.data.sensible_segment import SensibleSegment
from pinch.data.stream_enums import HeatType


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

    def test_heat_capacity_flow_rate(self):
        self.assertEqual(self.cold_segment.heat_capacity_flow_rate, 1)
        self.assertEqual(self.hot_segment.heat_capacity_flow_rate, 1.8)

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

    def test_min_temperature(self):
        self.assertEqual(self.cold_segment.min_temperature, 20)
        self.assertEqual(self.hot_segment.min_temperature, 50)

    def test_max_temperature(self):
        self.assertEqual(self.cold_segment.max_temperature, 200)
        self.assertEqual(self.hot_segment.max_temperature, 150)

    def test_split(self):
        # Cold stream
        heat_capacity_flow_rate = self.cold_segment.heat_capacity_flow_rate
        min_temp = self.cold_segment.min_temperature
        max_temp = self.cold_segment.max_temperature

        match_min_max = [20, 200]
        beyond_min_max = [-25, 430]
        below_min = [-10, 10]
        above_max = [250, 400, 600]
        include_min = [-10, 50]
        include_max = [150, 400, 600]
        within_min_max = [80, 120, 150]
        duplicates = [80, 120, 120]
        unsorted = [150, 80, 120]

        self.assertEqual(self.cold_segment.split([]), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(match_min_max), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(beyond_min_max), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(below_min), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(above_max), [self.cold_segment])

        self.assertEqual(
            self.cold_segment.split(include_min),
            [
                SensibleSegment(heat_capacity_flow_rate, min_temp, 50),
                SensibleSegment(heat_capacity_flow_rate, 50, max_temp)
            ]
        )

        self.assertEqual(
            self.cold_segment.split(include_max),
            [
                SensibleSegment(heat_capacity_flow_rate, min_temp, 150),
                SensibleSegment(heat_capacity_flow_rate, 150, max_temp)
            ]
        )

        self.assertEqual(
            self.cold_segment.split(within_min_max),
            [
                SensibleSegment(heat_capacity_flow_rate, min_temp, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, 150),
                SensibleSegment(heat_capacity_flow_rate, 150, max_temp)
            ]
        )

        self.assertEqual(
            self.cold_segment.split(duplicates),
            [
                SensibleSegment(heat_capacity_flow_rate, min_temp, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, max_temp)
            ]
        )

        self.assertEqual(
            self.cold_segment.split(unsorted),
            [
                SensibleSegment(heat_capacity_flow_rate, min_temp, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, 150),
                SensibleSegment(heat_capacity_flow_rate, 150, max_temp)
            ]
        )

        # Hot stream
        heat_capacity_flow_rate = self.hot_segment.heat_capacity_flow_rate
        min_temp = self.hot_segment.min_temperature
        max_temp = self.hot_segment.max_temperature

        match_min_max = [150, 50]
        beyond_min_max = [-25, 430]
        below_min = [-10, 10]
        above_max = [250, 400, 600]
        include_min = [-10, 80]
        include_max = [120, 400, 600]
        within_min_max = [80, 120, 135]
        duplicates = [80, 120, 120]
        unsorted = [150, 80, 120]

        self.assertEqual(self.hot_segment.split([]), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(match_min_max), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(beyond_min_max), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(below_min), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(above_max), [self.hot_segment])

        self.assertEqual(
            self.hot_segment.split(include_min),
            [
                SensibleSegment(heat_capacity_flow_rate, max_temp, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, min_temp)
            ]
        )

        self.assertEqual(
            self.hot_segment.split(include_max),
            [
                SensibleSegment(heat_capacity_flow_rate, max_temp, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, min_temp)
            ]
        )

        self.assertEqual(
            self.hot_segment.split(within_min_max),
            [
                SensibleSegment(heat_capacity_flow_rate, max_temp, 135),
                SensibleSegment(heat_capacity_flow_rate, 135, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, min_temp)
            ]
        )

        self.assertEqual(
            self.hot_segment.split(duplicates),
            [
                SensibleSegment(heat_capacity_flow_rate, max_temp, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, min_temp)
            ]
        )

        self.assertEqual(
            self.hot_segment.split(unsorted),
            [
                SensibleSegment(heat_capacity_flow_rate, max_temp, 120),
                SensibleSegment(heat_capacity_flow_rate, 120, 80),
                SensibleSegment(heat_capacity_flow_rate, 80, min_temp)
            ]
        )

    def test_equality_comparison(self):
        self.assertEqual(self.cold_segment, SensibleSegment(1, 20, 200))
        self.assertNotEqual(self.cold_segment, SensibleSegment(1, 20, 200, 8))
        self.assertNotEqual(self.cold_segment, SensibleSegment(2, 20, 200))
        self.assertNotEqual(self.cold_segment, SensibleSegment(1, 40, 200))
        self.assertNotEqual(self.cold_segment, SensibleSegment(1, 20, 150))
        self.assertNotEqual(self.cold_segment, LatentSegment(20, 180))
        self.assertNotEqual(self.cold_segment, LatentSegment(200, 180))

        self.assertEqual(self.hot_segment, SensibleSegment(1.8, 150, 50))
        self.assertNotEqual(self.hot_segment, SensibleSegment(1.8, 150, 50, 15))
        self.assertNotEqual(self.hot_segment, SensibleSegment(4, 150, 50))
        self.assertNotEqual(self.hot_segment, SensibleSegment(1.8, 240, 50))
        self.assertNotEqual(self.hot_segment, SensibleSegment(1.8, 150, 80))
        self.assertNotEqual(self.hot_segment, LatentSegment(-180, 150))
        self.assertNotEqual(self.hot_segment, LatentSegment(-180, 50))


if __name__ == "__main__":
    unittest.main()
