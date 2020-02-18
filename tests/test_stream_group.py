import unittest

from pinch import segment
from pinch.heat_cascade import HeatCascade
from pinch.stream import Stream
from pinch.stream_group import StreamGroup


class TestStreamGroup(unittest.TestCase):
    """
    Test class for StreamGroup
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        group = StreamGroup()
        self.assertEqual(group.cooling_demand, 0)
        self.assertEqual(group.heating_demand, 0)
        self.assertEqual(group.cold_utility_target, 0)
        self.assertEqual(group.hot_utility_target, 0)
        self.assertEqual(group.heat_recovery_target, 0)
        self.assertEqual(group.pinch_temps, [])
        self.assertEqual(group.default_temp_diff_contrib, None)
        self.assertEqual(group.streams, [])
        self.assertEqual(group.cold_cascade, HeatCascade())
        self.assertEqual(group.hot_cascade, HeatCascade())
        self.assertEqual(group.shifted_cold_cascade, HeatCascade())
        self.assertEqual(group.shifted_hot_cascade, HeatCascade())
        self.assertEqual(group.grand_cascade, HeatCascade())

    def test_2_stream_example(self):
        cold_segment = segment.new(-180, 20, 200)
        hot_segment = segment.new(180, 150, 50)
        cold_stream = Stream([cold_segment])
        hot_stream = Stream([hot_segment])
        group = StreamGroup(default_temp_diff_contrib=10)
        group.add([cold_stream, hot_stream])

        self.assertEqual(group.cooling_demand, 180)
        self.assertEqual(group.heating_demand, 180)
        self.assertEqual(group.cold_utility_target, 70)
        self.assertEqual(group.hot_utility_target, 70)
        self.assertEqual(group.heat_recovery_target, 110)
        self.assertEqual(group.pinch_temps, [140])
        self.assertEqual(group.default_temp_diff_contrib, 10)

        self.assertEqual(group.streams, [cold_stream, hot_stream])

        expected_cold_cascade = HeatCascade([
            cold_segment.with_absolute_heat_flow()])
        expected_cold_cascade.heat_offset = 70
        self.assertEqual(group.cold_cascade, expected_cold_cascade)

        expected_hot_cascade = HeatCascade([
            hot_segment.with_absolute_heat_flow()])
        expected_hot_cascade.heat_offset = 0
        self.assertEqual(group.hot_cascade, expected_hot_cascade)

        expected_shifted_cold_cascade = HeatCascade([
            cold_segment.shift(10).with_absolute_heat_flow()])
        expected_shifted_cold_cascade.heat_offset = 70
        self.assertEqual(
            group.shifted_cold_cascade, expected_shifted_cold_cascade)

        expected_shifted_hot_cascade = HeatCascade([
            hot_segment.shift(10).with_absolute_heat_flow()])
        expected_shifted_hot_cascade.heat_offset = 0
        self.assertEqual(
            group.shifted_hot_cascade, expected_shifted_hot_cascade)

        expected_grand_cascade = HeatCascade([
            cold_segment.shift(10).with_inverted_heat_flow(),
            hot_segment.shift(10).with_inverted_heat_flow()])
        expected_grand_cascade.heat_offset = 70
        self.assertEqual(group.grand_cascade, expected_grand_cascade)

    def test_extended_pinch(self):
        cold_segment = segment.new(-225, 20, 95)
        hot_segment = segment.new(267, 95, 6)
        cold_stream = Stream([cold_segment])
        hot_stream = Stream([hot_segment])
        group = StreamGroup(default_temp_diff_contrib=1)
        group.add([cold_stream, hot_stream])

        self.assertEqual(group.cooling_demand, 267)
        self.assertEqual(group.heating_demand, 225)
        self.assertEqual(group.cold_utility_target, 48)
        self.assertEqual(group.hot_utility_target, 6)
        self.assertEqual(group.heat_recovery_target, 219)
        self.assertEqual(group.pinch_temps, [21, 94])
        self.assertEqual(group.default_temp_diff_contrib, 1)

    def test_2_pinches(self):
        cold_stream = Stream([
            segment.new(-50, 50, 100),
            segment.new(-40, 100, 100),
            segment.new(-100, 100, 200)
        ])
        hot_stream = Stream([segment.new(260, 150, 20)])
        group = StreamGroup(default_temp_diff_contrib=5)
        group.add([cold_stream, hot_stream])

        self.assertEqual(group.cooling_demand, 260)
        self.assertEqual(group.heating_demand, 190)
        self.assertEqual(group.cold_utility_target, 130)
        self.assertEqual(group.hot_utility_target, 60)
        self.assertEqual(group.heat_recovery_target, 130)
        self.assertEqual(group.pinch_temps, [105, 145])
        self.assertEqual(group.default_temp_diff_contrib, 5)

    def test_cold_stream_only(self):
        cold_stream = Stream([segment.new(-40, 100, 100)])
        group = StreamGroup(default_temp_diff_contrib=5)
        group.add([cold_stream])

        self.assertEqual(group.cooling_demand, 0)
        self.assertEqual(group.heating_demand, 40)
        self.assertEqual(group.cold_utility_target, 0)
        self.assertEqual(group.hot_utility_target, 40)
        self.assertEqual(group.heat_recovery_target, 0)
        self.assertEqual(group.pinch_temps, [105])
        self.assertEqual(group.default_temp_diff_contrib, 5)

    def test_hot_stream_only(self):
        hot_stream = Stream([segment.new(260, 150, 20)])
        group = StreamGroup(default_temp_diff_contrib=5)
        group.add([hot_stream])

        self.assertEqual(group.cooling_demand, 260)
        self.assertEqual(group.heating_demand, 0)
        self.assertEqual(group.cold_utility_target, 260)
        self.assertEqual(group.hot_utility_target, 0)
        self.assertEqual(group.heat_recovery_target, 0)
        self.assertEqual(group.pinch_temps, [145])
        self.assertEqual(group.default_temp_diff_contrib, 5)

    def test_individual_temp_diff_contrib(self):
        cold_stream = Stream([segment.new(-40, 100, 100, 10)])
        group = StreamGroup(default_temp_diff_contrib=5)
        group.add([cold_stream])

        self.assertEqual(group.cooling_demand, 0)
        self.assertEqual(group.heating_demand, 40)
        self.assertEqual(group.cold_utility_target, 0)
        self.assertEqual(group.hot_utility_target, 40)
        self.assertEqual(group.heat_recovery_target, 0)
        self.assertEqual(group.pinch_temps, [110])
        self.assertEqual(group.default_temp_diff_contrib, 5)


if __name__ == "__main__":
    unittest.main()
