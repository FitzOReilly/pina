import unittest

from pina.enums import HeatType
from pina.segments.latent_segment import LatentSegment
from pina.segments.sensible_segment import SensibleSegment


class TestLatentSegment(unittest.TestCase):
    """
    Test class for LatentSegment
    """

    def setUp(self):
        self.neutral_segment = LatentSegment(0, 80)
        self.cold_segment = LatentSegment(-200, 100)
        self.hot_segment = LatentSegment(300, 150)

    def tearDown(self):
        pass

    def test_heat_type(self):
        self.assertEqual(self.neutral_segment.heat_type, HeatType.LATENT)
        self.assertEqual(self.cold_segment.heat_type, HeatType.LATENT)
        self.assertEqual(self.hot_segment.heat_type, HeatType.LATENT)

    def test_supply_temp(self):
        self.assertEqual(self.neutral_segment.supply_temp, 80)
        self.assertEqual(self.cold_segment.supply_temp, 100)
        self.assertEqual(self.hot_segment.supply_temp, 150)

    def test_target_temp(self):
        self.assertEqual(self.neutral_segment.target_temp, 80)
        self.assertEqual(self.cold_segment.target_temp, 100)
        self.assertEqual(self.hot_segment.target_temp, 150)

    def test_heat_flow(self):
        self.assertEqual(self.neutral_segment.heat_flow, 0)
        self.assertEqual(self.cold_segment.heat_flow, -200)
        self.assertEqual(self.hot_segment.heat_flow, 300)

    def test_default_temp_shift(self):
        self.assertEqual(self.neutral_segment.temp_shift, None)
        self.assertEqual(self.cold_segment.temp_shift, None)
        self.assertEqual(self.hot_segment.temp_shift, None)

    def test_temp_shift(self):
        segment = LatentSegment(100, 200, 10)
        self.assertEqual(segment.temp_shift, 10)

    def test_min_and_max_temps(self):
        self.assertEqual(self.neutral_segment.min_temp, 80)
        self.assertEqual(self.neutral_segment.max_temp, 80)
        self.assertEqual(self.cold_segment.min_temp, 100)
        self.assertEqual(self.cold_segment.max_temp, 100)
        self.assertEqual(self.hot_segment.min_temp, 150)
        self.assertEqual(self.hot_segment.max_temp, 150)

    def test_new_equal_temps(self):
        self.assertEqual(
            LatentSegment.new(400, 100, 100), LatentSegment(400, 100, None)
        )
        self.assertEqual(LatentSegment.new(-500, 0, 0, 10), LatentSegment(-500, 0, 10))

    def test_new_different_temps(self):
        with self.assertRaises(ValueError):
            LatentSegment.new(400, 100, 150)
        with self.assertRaises(ValueError):
            LatentSegment.new(-500, 0, -50, 10)

    def test_clone(self):
        original = LatentSegment.new(400, 100, 100)
        clone = original.clone()
        self.assertEqual(original, clone)
        self.assertIsNot(original, clone)

        original = LatentSegment.new(-500, 0, 0, 10)
        clone = original.clone()
        self.assertEqual(original, clone)
        self.assertIsNot(original, clone)

    def test_shift_no_temp_shift_given(self):
        self.assertEqual(LatentSegment(0, 80).shift(), LatentSegment(0, 80, 0))
        with self.assertRaises(ValueError):
            LatentSegment(-200, 100).shift()
        with self.assertRaises(ValueError):
            LatentSegment(300, 150).shift()

    def test_shift_self_temp_shift(self):
        self.assertEqual(LatentSegment(0, 80, 10).shift(), LatentSegment(0, 80, 0))
        self.assertEqual(
            LatentSegment(-200, 100, 10).shift(), LatentSegment(-200, 110, 0)
        )
        self.assertEqual(
            LatentSegment(300, 150, 10).shift(), LatentSegment(300, 140, 0)
        )

    def test_shift_default_temp_shift(self):
        self.assertEqual(LatentSegment(0, 80).shift(5), LatentSegment(0, 80, 0))
        self.assertEqual(LatentSegment(-200, 100).shift(5), LatentSegment(-200, 105, 0))
        self.assertEqual(LatentSegment(300, 150).shift(5), LatentSegment(300, 145, 0))

    def test_shift_self_and_default_temp_shift(self):
        self.assertEqual(LatentSegment(0, 80, 10).shift(5), LatentSegment(0, 80, 0))
        self.assertEqual(
            LatentSegment(-200, 100, 10).shift(5), LatentSegment(-200, 110, 0)
        )
        self.assertEqual(
            LatentSegment(300, 150, 10).shift(5), LatentSegment(300, 140, 0)
        )

    def test_split(self):
        self.assertEqual(self.neutral_segment.split([]), [self.neutral_segment])
        self.assertEqual(
            self.neutral_segment.split([50, 80, 90]), [self.neutral_segment]
        )

        segment_temp_included = [100, 150]
        segment_temp_not_included = [90, 140]
        self.assertEqual(self.cold_segment.split([]), [self.cold_segment])
        self.assertEqual(
            self.cold_segment.split(segment_temp_included), [self.cold_segment]
        )
        self.assertEqual(
            self.cold_segment.split(segment_temp_not_included), [self.cold_segment]
        )

        self.assertEqual(self.hot_segment.split([]), [self.hot_segment])
        self.assertEqual(
            self.hot_segment.split(segment_temp_included), [self.hot_segment]
        )
        self.assertEqual(
            self.hot_segment.split(segment_temp_not_included), [self.hot_segment]
        )

    def test_with_low_supply_temp(self):
        self.assertEqual(
            self.neutral_segment.with_low_supply_temp(), self.neutral_segment
        )
        self.assertEqual(self.cold_segment.with_low_supply_temp(), self.cold_segment)
        self.assertEqual(self.hot_segment.with_low_supply_temp(), self.hot_segment)

    def test_with_absolute_heat_flow(self):
        self.assertEqual(
            LatentSegment(0, 80).with_absolute_heat_flow(), LatentSegment(0, 80)
        )
        self.assertEqual(
            LatentSegment(-200, 100).with_absolute_heat_flow(), LatentSegment(200, 100)
        )
        self.assertEqual(
            LatentSegment(-200, 100, 5).with_absolute_heat_flow(),
            LatentSegment(200, 100, 5),
        )
        self.assertEqual(
            LatentSegment(300, 150).with_absolute_heat_flow(), LatentSegment(300, 150)
        )
        self.assertEqual(
            LatentSegment(300, 150, 10).with_absolute_heat_flow(),
            LatentSegment(300, 150, 10),
        )

    def test_with_inverted_heat_flow(self):
        self.assertEqual(
            LatentSegment(0, 80).with_inverted_heat_flow(), LatentSegment(0, 80)
        )
        self.assertEqual(
            LatentSegment(-200, 100).with_inverted_heat_flow(), LatentSegment(200, 100)
        )
        self.assertEqual(
            LatentSegment(-200, 100, 5).with_inverted_heat_flow(),
            LatentSegment(200, 100, 5),
        )
        self.assertEqual(
            LatentSegment(300, 150).with_inverted_heat_flow(), LatentSegment(-300, 150)
        )
        self.assertEqual(
            LatentSegment(300, 150, 10).with_inverted_heat_flow(),
            LatentSegment(-300, 150, 10),
        )

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
            self.neutral_segment.add(self.neutral_segment), LatentSegment(0, 80)
        )

        self.assertEqual(
            LatentSegment(200, 100).add(LatentSegment(50, 100)), LatentSegment(250, 100)
        )
        self.assertEqual(
            LatentSegment(200, 100, 20).add(LatentSegment(-150, 100, 5), 10),
            LatentSegment(50, 100, 10),
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
            self.neutral_segment.link(self.neutral_segment), LatentSegment(0, 80)
        )

        self.assertEqual(
            LatentSegment(200, 100).link(LatentSegment(50, 100)),
            LatentSegment(250, 100),
        )
        self.assertEqual(
            LatentSegment(200, 100, 20).link(LatentSegment(-150, 100, 5), 10),
            LatentSegment(50, 100, 10),
        )

    def test_equality_comparison(self):
        self.assertEqual(self.neutral_segment, LatentSegment(0, 80))
        self.assertNotEqual(self.neutral_segment, LatentSegment(0, 80, 10))
        self.assertNotEqual(self.neutral_segment, LatentSegment(100, 80))
        self.assertNotEqual(self.neutral_segment, LatentSegment(0, 120))
        self.assertNotEqual(self.neutral_segment, SensibleSegment(2, 50, 200))

        self.assertEqual(self.cold_segment, LatentSegment(-200, 100))
        self.assertNotEqual(self.cold_segment, LatentSegment(-200, 100, 10))
        self.assertNotEqual(self.cold_segment, LatentSegment(-300, 100))
        self.assertNotEqual(self.cold_segment, LatentSegment(-200, 150))
        self.assertNotEqual(self.cold_segment, SensibleSegment(4, 100, 150))

        self.assertEqual(self.hot_segment, LatentSegment(300, 150))
        self.assertNotEqual(self.hot_segment, LatentSegment(300, 150, 5))
        self.assertNotEqual(self.hot_segment, LatentSegment(200, 150))
        self.assertNotEqual(self.hot_segment, LatentSegment(300, 240))
        self.assertNotEqual(self.cold_segment, SensibleSegment(6, 150, 100))


if __name__ == "__main__":
    unittest.main()
