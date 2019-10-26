import unittest

from pinch.latent_segment import LatentSegment
from pinch.sensible_segment import SensibleSegment
from pinch.stream_enums import HeatType


class TestSensibleSegment(unittest.TestCase):
    """
    Test class for SensibleSegment
    """

    def setUp(self):
        self.neutral_segment = SensibleSegment(2, 50, 50)
        self.zero_capacity_segment = SensibleSegment(0, 80, 120)
        self.cold_segment = SensibleSegment(1, 20, 200)
        self.hot_segment = SensibleSegment(1.8, 150, 50)

    def tearDown(self):
        pass

    def test_heat_type(self):
        self.assertEqual(self.neutral_segment.heat_type, HeatType.SENSIBLE)
        self.assertEqual(self.zero_capacity_segment.heat_type, HeatType.SENSIBLE)
        self.assertEqual(self.cold_segment.heat_type, HeatType.SENSIBLE)
        self.assertEqual(self.hot_segment.heat_type, HeatType.SENSIBLE)

    def test_heat_capacity_flow_rate(self):
        self.assertEqual(self.neutral_segment.heat_capacity_flow_rate, 2)
        self.assertEqual(self.zero_capacity_segment.heat_capacity_flow_rate, 0)
        self.assertEqual(self.cold_segment.heat_capacity_flow_rate, 1)
        self.assertEqual(self.hot_segment.heat_capacity_flow_rate, 1.8)

    def test_supply_temperature(self):
        self.assertEqual(self.neutral_segment.supply_temperature, 50)
        self.assertEqual(self.zero_capacity_segment.supply_temperature, 80)
        self.assertEqual(self.cold_segment.supply_temperature, 20)
        self.assertEqual(self.hot_segment.supply_temperature, 150)

    def test_target_temperature(self):
        self.assertEqual(self.neutral_segment.target_temperature, 50)
        self.assertEqual(self.zero_capacity_segment.target_temperature, 120)
        self.assertEqual(self.cold_segment.target_temperature, 200)
        self.assertEqual(self.hot_segment.target_temperature, 50)

    def test_heat_flow(self):
        self.assertEqual(self.neutral_segment.heat_flow, 0)
        self.assertEqual(self.zero_capacity_segment.heat_flow, 0)
        self.assertEqual(self.cold_segment.heat_flow, 180)
        self.assertEqual(self.hot_segment.heat_flow, -180)

    def test_default_temperature_difference_contribution(self):
        self.assertEqual(self.cold_segment.temperature_difference_contribution, None)
        self.assertEqual(self.hot_segment.temperature_difference_contribution, None)

    def test_temperature_difference_contribution(self):
        segment = SensibleSegment(1, 20, 200, 5)
        self.assertEqual(segment.temperature_difference_contribution, 5)

    def test_min_temperature(self):
        self.assertEqual(self.neutral_segment.min_temperature, 50)
        self.assertEqual(self.zero_capacity_segment.min_temperature, 80)
        self.assertEqual(self.cold_segment.min_temperature, 20)
        self.assertEqual(self.hot_segment.min_temperature, 50)

    def test_max_temperature(self):
        self.assertEqual(self.neutral_segment.max_temperature, 50)
        self.assertEqual(self.zero_capacity_segment.max_temperature, 120)
        self.assertEqual(self.cold_segment.max_temperature, 200)
        self.assertEqual(self.hot_segment.max_temperature, 150)

    def test_shift_no_temperature_difference_contribution_given(self):
        self.assertEqual(SensibleSegment(2, 50, 50).shift(), SensibleSegment(2, 50, 50, 0))
        self.assertEqual(SensibleSegment(0, 80, 120).shift(), SensibleSegment(0, 80, 120, 0))
        with self.assertRaises(ValueError):
            SensibleSegment(1, 20, 200).shift()
        with self.assertRaises(ValueError):
            SensibleSegment(1.8, 150, 50).shift()

    def test_shift_self_temperature_difference_contribution(self):
        self.assertEqual(SensibleSegment(2, 50, 50, 10).shift(), SensibleSegment(2, 50, 50, 0))
        self.assertEqual(SensibleSegment(0, 80, 120, 10).shift(), SensibleSegment(0, 80, 120, 0))
        self.assertEqual(SensibleSegment(1, 20, 200, 10).shift(), SensibleSegment(1, 30, 210, 0))
        self.assertEqual(SensibleSegment(1.8, 150, 50, 10).shift(), SensibleSegment(1.8, 140, 40, 0))

    def test_shift_default_temperature_difference_contribution(self):
        self.assertEqual(SensibleSegment(2, 50, 50).shift(5), SensibleSegment(2, 50, 50, 0))
        self.assertEqual(SensibleSegment(0, 80, 120).shift(5), SensibleSegment(0, 80, 120, 0))
        self.assertEqual(SensibleSegment(1, 20, 200).shift(5), SensibleSegment(1, 25, 205, 0))
        self.assertEqual(SensibleSegment(1.8, 150, 50).shift(5), SensibleSegment(1.8, 145, 45, 0))

    def test_shift_self_and_default_temperature_difference_contribution_(self):
        self.assertEqual(SensibleSegment(2, 50, 50, 10).shift(5), SensibleSegment(2, 50, 50, 0))
        self.assertEqual(SensibleSegment(0, 80, 120, 10).shift(5), SensibleSegment(0, 80, 120, 0))
        self.assertEqual(SensibleSegment(1, 20, 200, 10).shift(5), SensibleSegment(1, 30, 210, 0))
        self.assertEqual(SensibleSegment(1.8, 150, 50, 10).shift(5), SensibleSegment(1.8, 140, 40, 0))

    def test_split(self):
        # Neutral segment
        self.assertEqual(self.neutral_segment.split([]), [self.neutral_segment])
        self.assertEqual(self.neutral_segment.split([10, 50, 100]), [self.neutral_segment])

        # Neutral segment with zero heat capacity flow rate
        self.assertEqual(self.zero_capacity_segment.split([]), [self.zero_capacity_segment])
        self.assertEqual(
            self.zero_capacity_segment.split([10, 50, 100]),
            [
                SensibleSegment(0, 80, 100),
                SensibleSegment(0, 100, 120)
            ]
        )

        # Cold segment
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

        # Hot segment
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

    def test_with_low_supply_temperature(self):
        self.assertEqual(self.neutral_segment.with_low_supply_temperature(), self.neutral_segment)
        self.assertEqual(self.cold_segment.with_low_supply_temperature(), self.cold_segment)
        self.assertEqual(self.hot_segment.with_low_supply_temperature(), SensibleSegment(-1.8, 50, 150))

    def test_with_absolute_heat_flow(self):
        self.assertEqual(SensibleSegment(2, 50, 50).with_absolute_heat_flow(), SensibleSegment(2, 50, 50))
        self.assertEqual(SensibleSegment(0, 80, 120).with_absolute_heat_flow(), SensibleSegment(0, 80, 120))
        self.assertEqual(SensibleSegment(1, 20, 200).with_absolute_heat_flow(), SensibleSegment(1, 20, 200))
        self.assertEqual(SensibleSegment(-1, 20, 200, 5).with_absolute_heat_flow(), SensibleSegment(1, 20, 200, 5))
        self.assertEqual(SensibleSegment(1.8, 150, 50).with_absolute_heat_flow(), SensibleSegment(-1.8, 150, 50))
        self.assertEqual(SensibleSegment(-1.8, 150, 50).with_absolute_heat_flow(), SensibleSegment(-1.8, 150, 50))
        self.assertEqual(SensibleSegment(1.8, 150, 50, 10).with_absolute_heat_flow(), SensibleSegment(-1.8, 150, 50, 10))

    def test_with_inverted_heat_flow(self):
        self.assertEqual(SensibleSegment(2, 50, 50).with_inverted_heat_flow(), SensibleSegment(-2, 50, 50))
        self.assertEqual(SensibleSegment(0, 80, 120).with_inverted_heat_flow(), SensibleSegment(0, 80, 120))
        self.assertEqual(SensibleSegment(1, 20, 200).with_inverted_heat_flow(), SensibleSegment(-1, 20, 200))
        self.assertEqual(SensibleSegment(-1, 20, 200, 5).with_inverted_heat_flow(), SensibleSegment(1, 20, 200, 5))
        self.assertEqual(SensibleSegment(1.8, 150, 50).with_inverted_heat_flow(), SensibleSegment(-1.8, 150, 50))
        self.assertEqual(SensibleSegment(-1.8, 150, 50).with_inverted_heat_flow(), SensibleSegment(1.8, 150, 50))
        self.assertEqual(SensibleSegment(1.8, 150, 50, 10).with_inverted_heat_flow(), SensibleSegment(-1.8, 150, 50, 10))

    def test_add_if_possible(self):
        self.assertIsNone(self.cold_segment.add_if_possible(self.neutral_segment))
        self.assertIsNone(self.neutral_segment.add_if_possible(self.hot_segment))
        self.assertIsNone(self.cold_segment.add_if_possible(self.hot_segment))
        self.assertIsNone(self.hot_segment.add_if_possible(self.cold_segment, 10))

        self.assertEqual(
            self.neutral_segment.add_if_possible(self.neutral_segment),
            SensibleSegment(4, 50, 50)
        )
        self.assertEqual(
            SensibleSegment(2, 100, 180).add_if_possible(SensibleSegment(0, 100, 180)),
            SensibleSegment(2, 100, 180)
        )
        self.assertEqual(
            SensibleSegment(0, 100, 180).add_if_possible(SensibleSegment(2, 100, 180)),
            SensibleSegment(2, 100, 180)
        )
        self.assertEqual(
            SensibleSegment(2, 100, 180).add_if_possible(SensibleSegment(5, 100, 180)),
            SensibleSegment(7, 100, 180)
        )
        self.assertEqual(
            SensibleSegment(4, 100, 180, 2).add_if_possible(SensibleSegment(2.5, 180, 100, 5), 10),
            SensibleSegment(1.5, 100, 180, 10)
        )

    def test_merge_if_possible(self):
        self.assertIsNone(self.cold_segment.merge_if_possible(self.neutral_segment))
        self.assertIsNone(self.cold_segment.merge_if_possible(self.hot_segment))
        self.assertIsNone(self.hot_segment.merge_if_possible(self.cold_segment, 10))
        self.assertIsNone(SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(5, 100, 180)))
        self.assertIsNone(SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(5, 150, 220, 5)))
        self.assertIsNone(SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(5, 180, 240)))
        self.assertIsNone(SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(-2, 180, 220)))

        self.assertEqual(
            self.neutral_segment.merge_if_possible(self.neutral_segment),
            SensibleSegment(2, 50, 50)
        )
        self.assertEqual(
            SensibleSegment(0, 80, 180).merge_if_possible(SensibleSegment(0, 180, 120)),
            SensibleSegment(0, 80, 120)
        )
        self.assertEqual(
            SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(2, 180, 220)),
            SensibleSegment(2, 100, 220)
        )
        self.assertEqual(
            SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(2, 180, 140), 5),
            SensibleSegment(2, 100, 140, 5)
        )
        self.assertEqual(
            SensibleSegment(2, 100, 180).merge_if_possible(SensibleSegment(2, 180, 100)),
            SensibleSegment(2, 100, 100)
        )

    def test_equality_comparison(self):
        self.assertEqual(self.neutral_segment, SensibleSegment(2, 50, 50))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(2, 50, 50, 5))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(3.5, 50, 50))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(2, 40, 50))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(2, 50, 40))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(2, 40, 40))
        self.assertNotEqual(self.neutral_segment, LatentSegment(0, 50))

        self.assertEqual(self.zero_capacity_segment, SensibleSegment(0, 80, 120))
        self.assertNotEqual(self.zero_capacity_segment, SensibleSegment(0, 80, 120, 5))
        self.assertNotEqual(self.zero_capacity_segment, SensibleSegment(3.5, 80, 120))
        self.assertNotEqual(self.zero_capacity_segment, SensibleSegment(0, 40, 120))
        self.assertNotEqual(self.zero_capacity_segment, SensibleSegment(0, 80, 40))
        self.assertNotEqual(self.zero_capacity_segment, LatentSegment(0, 80))
        self.assertNotEqual(self.zero_capacity_segment, LatentSegment(0, 120))

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
