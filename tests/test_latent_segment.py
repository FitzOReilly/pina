import unittest

from pinch.latent_segment import LatentSegment
from pinch.sensible_segment import SensibleSegment
from pinch.stream_enums import HeatType


class TestLatentSegment(unittest.TestCase):
    """
    Test class for LatentSegment
    """
    def setUp(self):
        self.neutral_segment = LatentSegment(0, 80)
        self.cold_segment = LatentSegment(200, 100)
        self.hot_segment = LatentSegment(-300, 150)

    def tearDown(self):
        pass

    def test_heat_type(self):
        self.assertEqual(self.neutral_segment.heat_type, HeatType.LATENT)
        self.assertEqual(self.cold_segment.heat_type, HeatType.LATENT)
        self.assertEqual(self.hot_segment.heat_type, HeatType.LATENT)

    def test_supply_temperature(self):
        self.assertEqual(self.neutral_segment.supply_temperature, 80)
        self.assertEqual(self.cold_segment.supply_temperature, 100)
        self.assertEqual(self.hot_segment.supply_temperature, 150)

    def test_target_temperature(self):
        self.assertEqual(self.neutral_segment.target_temperature, 80)
        self.assertEqual(self.cold_segment.target_temperature, 100)
        self.assertEqual(self.hot_segment.target_temperature, 150)

    def test_heat_flow(self):
        self.assertEqual(self.neutral_segment.heat_flow, 0)
        self.assertEqual(self.cold_segment.heat_flow, 200)
        self.assertEqual(self.hot_segment.heat_flow, -300)

    def test_default_temperature_difference_contribution(self):
        self.assertEqual(self.neutral_segment.temperature_difference_contribution, None)
        self.assertEqual(self.cold_segment.temperature_difference_contribution, None)
        self.assertEqual(self.hot_segment.temperature_difference_contribution, None)

    def test_temperature_difference_contribution(self):
        segment = LatentSegment(100, 200, 10)
        self.assertEqual(segment.temperature_difference_contribution, 10)

    def test_min_and_max_temperatures(self):
        self.assertEqual(self.neutral_segment.min_temperature, 80)
        self.assertEqual(self.neutral_segment.max_temperature, 80)
        self.assertEqual(self.cold_segment.min_temperature, 100)
        self.assertEqual(self.cold_segment.max_temperature, 100)
        self.assertEqual(self.hot_segment.min_temperature, 150)
        self.assertEqual(self.hot_segment.max_temperature, 150)

    def test_shift_no_temperature_difference_contribution_given(self):
        self.assertEqual(LatentSegment(0, 80).shift(), LatentSegment(0, 80, 0))
        with self.assertRaises(ValueError):
            LatentSegment(200, 100).shift()
        with self.assertRaises(ValueError):
            LatentSegment(-300, 150).shift()

    def test_shift_self_temperature_difference_contribution(self):
        self.assertEqual(LatentSegment(0, 80, 10).shift(), LatentSegment(0, 80, 0))
        self.assertEqual(LatentSegment(200, 100, 10).shift(), LatentSegment(200, 110, 0))
        self.assertEqual(LatentSegment(-300, 150, 10).shift(), LatentSegment(-300, 140, 0))

    def test_shift_default_temperature_difference_contribution(self):
        self.assertEqual(LatentSegment(0, 80).shift(5), LatentSegment(0, 80, 0))
        self.assertEqual(LatentSegment(200, 100).shift(5), LatentSegment(200, 105, 0))
        self.assertEqual(LatentSegment(-300, 150).shift(5), LatentSegment(-300, 145, 0))

    def test_shift_self_and_default_temperature_difference_contribution_(self):
        self.assertEqual(LatentSegment(0, 80, 10).shift(5), LatentSegment(0, 80, 0))
        self.assertEqual(LatentSegment(200, 100, 10).shift(5), LatentSegment(200, 110, 0))
        self.assertEqual(LatentSegment(-300, 150, 10).shift(5), LatentSegment(-300, 140, 0))

    def test_split(self):
        self.assertEqual(self.neutral_segment.split([]), [self.neutral_segment])
        self.assertEqual(self.neutral_segment.split([50, 80, 90]), [self.neutral_segment])

        segment_temp_included = [100, 150]
        segment_temp_not_included = [90, 140]
        self.assertEqual(self.cold_segment.split([]), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(segment_temp_included), [self.cold_segment])
        self.assertEqual(self.cold_segment.split(segment_temp_not_included), [self.cold_segment])

        self.assertEqual(self.hot_segment.split([]), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(segment_temp_included), [self.hot_segment])
        self.assertEqual(self.hot_segment.split(segment_temp_not_included), [self.hot_segment])

    def test_with_low_supply_temperature(self):
        self.assertEqual(self.neutral_segment.with_low_supply_temperature(), self.neutral_segment)
        self.assertEqual(self.cold_segment.with_low_supply_temperature(), self.cold_segment)
        self.assertEqual(self.hot_segment.with_low_supply_temperature(), self.hot_segment)

    def test_with_absolute_heat_flow(self):
        self.assertEqual(LatentSegment(0, 80).with_absolute_heat_flow(), LatentSegment(0, 80))
        self.assertEqual(LatentSegment(200, 100).with_absolute_heat_flow(), LatentSegment(200, 100))
        self.assertEqual(LatentSegment(200, 100, 5).with_absolute_heat_flow(), LatentSegment(200, 100, 5))
        self.assertEqual(LatentSegment(-300, 150).with_absolute_heat_flow(), LatentSegment(300, 150))
        self.assertEqual(LatentSegment(-300, 150, 10).with_absolute_heat_flow(), LatentSegment(300, 150, 10))

    def test_with_inverted_heat_flow(self):
        self.assertEqual(LatentSegment(0, 80).with_inverted_heat_flow(), LatentSegment(0, 80))
        self.assertEqual(LatentSegment(200, 100).with_inverted_heat_flow(), LatentSegment(-200, 100))
        self.assertEqual(LatentSegment(200, 100, 5).with_inverted_heat_flow(), LatentSegment(-200, 100, 5))
        self.assertEqual(LatentSegment(-300, 150).with_inverted_heat_flow(), LatentSegment(300, 150))
        self.assertEqual(LatentSegment(-300, 150, 10).with_inverted_heat_flow(), LatentSegment(300, 150, 10))

    def test_add(self):
        with self.assertRaises(ValueError):
            self.cold_segment.add(self.neutral_segment)
        with self.assertRaises(ValueError):
            self.neutral_segment.add(self.hot_segment)
        with self.assertRaises(ValueError):
            self.cold_segment.add(self.hot_segment)
        with self.assertRaises(ValueError):
            self.hot_segment.add(self.cold_segment, 10)

        self.assertEqual(
            self.neutral_segment.add(self.neutral_segment),
            LatentSegment(0, 80)
        )

        self.assertEqual(
            LatentSegment(200, 100).add(LatentSegment(50, 100)),
            LatentSegment(250, 100)
        )
        self.assertEqual(
            LatentSegment(200, 100, 20).add(LatentSegment(-150, 100, 5), 10),
            LatentSegment(50, 100, 10)
        )

    def test_link(self):
        with self.assertRaises(ValueError):
            self.cold_segment.link(self.neutral_segment)
        with self.assertRaises(ValueError):
            self.neutral_segment.link(self.hot_segment)
        with self.assertRaises(ValueError):
            self.cold_segment.link(self.hot_segment)
        with self.assertRaises(ValueError):
            self.hot_segment.link(self.cold_segment, 10)

        self.assertEqual(
            self.neutral_segment.link(self.neutral_segment),
            LatentSegment(0, 80)
        )

        self.assertEqual(
            LatentSegment(200, 100).link(LatentSegment(50, 100)),
            LatentSegment(250, 100)
        )
        self.assertEqual(
            LatentSegment(200, 100, 20).link(LatentSegment(-150, 100, 5), 10),
            LatentSegment(50, 100, 10)
        )

    def test_equality_comparison(self):
        self.assertEqual(self.neutral_segment, LatentSegment(0, 80))
        self.assertNotEqual(self.neutral_segment, LatentSegment(0, 80, 10))
        self.assertNotEqual(self.neutral_segment, LatentSegment(100, 80))
        self.assertNotEqual(self.neutral_segment, LatentSegment(0, 120))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(2, 50, 200))

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
