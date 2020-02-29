import unittest

from pinch import segment
from pinch.heat_cascade import HeatCascade
from pinch.stream import Stream
from pinch.stream_analyzer import StreamAnalyzer


class TestStreamAnalyzer(unittest.TestCase):
    """
    Test class for StreamAnalyzer
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        analyzer = StreamAnalyzer()
        self.assertEqual(analyzer.cooling_demand, 0)
        self.assertEqual(analyzer.heating_demand, 0)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 0)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [])
        self.assertEqual(analyzer.default_temp_shift, None)
        self.assertEqual(analyzer.streams, [])
        self.assertEqual(analyzer.cold_cascade, HeatCascade())
        self.assertEqual(analyzer.hot_cascade, HeatCascade())
        self.assertEqual(analyzer.shifted_cold_cascade, HeatCascade())
        self.assertEqual(analyzer.shifted_hot_cascade, HeatCascade())
        self.assertEqual(analyzer.grand_cascade, HeatCascade())

    def test_2_stream_example(self):
        cold_segment = segment.new(-180, 20, 200)
        hot_segment = segment.new(180, 150, 50)
        cold_stream = Stream([cold_segment])
        hot_stream = Stream([hot_segment])
        analyzer = StreamAnalyzer(default_temp_shift=10)
        analyzer.add([cold_stream, hot_stream])

        self.assertEqual(analyzer.cooling_demand, 180)
        self.assertEqual(analyzer.heating_demand, 180)
        self.assertEqual(analyzer.cold_utility_target, 70)
        self.assertEqual(analyzer.hot_utility_target, 70)
        self.assertEqual(analyzer.heat_recovery_target, 110)
        self.assertEqual(analyzer.pinch_temps, [140])
        self.assertEqual(analyzer.default_temp_shift, 10)

        self.assertEqual(analyzer.streams, [cold_stream, hot_stream])

        expected_cold_cascade = HeatCascade([
            cold_segment.with_absolute_heat_flow()])
        expected_cold_cascade.heat_offset = 70
        self.assertEqual(analyzer.cold_cascade, expected_cold_cascade)

        expected_hot_cascade = HeatCascade([
            hot_segment.with_absolute_heat_flow()])
        expected_hot_cascade.heat_offset = 0
        self.assertEqual(analyzer.hot_cascade, expected_hot_cascade)

        expected_shifted_cold_cascade = HeatCascade([
            cold_segment.shift(10).with_absolute_heat_flow()])
        expected_shifted_cold_cascade.heat_offset = 70
        self.assertEqual(
            analyzer.shifted_cold_cascade, expected_shifted_cold_cascade)

        expected_shifted_hot_cascade = HeatCascade([
            hot_segment.shift(10).with_absolute_heat_flow()])
        expected_shifted_hot_cascade.heat_offset = 0
        self.assertEqual(
            analyzer.shifted_hot_cascade, expected_shifted_hot_cascade)

        expected_grand_cascade = HeatCascade([
            cold_segment.shift(10).with_inverted_heat_flow(),
            hot_segment.shift(10).with_inverted_heat_flow()])
        expected_grand_cascade.heat_offset = 70
        self.assertEqual(analyzer.grand_cascade, expected_grand_cascade)

    def test_extended_pinch(self):
        cold_segment = segment.new(-225, 20, 95)
        hot_segment = segment.new(267, 95, 6)
        cold_stream = Stream([cold_segment])
        hot_stream = Stream([hot_segment])
        analyzer = StreamAnalyzer(default_temp_shift=1)
        analyzer.add([cold_stream, hot_stream])

        self.assertEqual(analyzer.cooling_demand, 267)
        self.assertEqual(analyzer.heating_demand, 225)
        self.assertEqual(analyzer.cold_utility_target, 48)
        self.assertEqual(analyzer.hot_utility_target, 6)
        self.assertEqual(analyzer.heat_recovery_target, 219)
        self.assertEqual(analyzer.pinch_temps, [21, 94])
        self.assertEqual(analyzer.default_temp_shift, 1)

    def test_2_pinches(self):
        cold_stream = Stream([
            segment.new(-50, 50, 100),
            segment.new(-40, 100, 100),
            segment.new(-100, 100, 200)
        ])
        hot_stream = Stream([segment.new(260, 150, 20)])
        analyzer = StreamAnalyzer(default_temp_shift=5)
        analyzer.add([cold_stream, hot_stream])

        self.assertEqual(analyzer.cooling_demand, 260)
        self.assertEqual(analyzer.heating_demand, 190)
        self.assertEqual(analyzer.cold_utility_target, 130)
        self.assertEqual(analyzer.hot_utility_target, 60)
        self.assertEqual(analyzer.heat_recovery_target, 130)
        self.assertEqual(analyzer.pinch_temps, [105, 145])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_cold_stream_only(self):
        cold_stream = Stream([segment.new(-40, 100, 100)])
        analyzer = StreamAnalyzer(default_temp_shift=5)
        analyzer.add([cold_stream])

        self.assertEqual(analyzer.cooling_demand, 0)
        self.assertEqual(analyzer.heating_demand, 40)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 40)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [105])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_hot_stream_only(self):
        hot_stream = Stream([segment.new(260, 150, 20)])
        analyzer = StreamAnalyzer(default_temp_shift=5)
        analyzer.add([hot_stream])

        self.assertEqual(analyzer.cooling_demand, 260)
        self.assertEqual(analyzer.heating_demand, 0)
        self.assertEqual(analyzer.cold_utility_target, 260)
        self.assertEqual(analyzer.hot_utility_target, 0)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [145])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_individual_temp_shift(self):
        cold_stream = Stream([segment.new(-40, 100, 100, 10)])
        analyzer = StreamAnalyzer(default_temp_shift=5)
        analyzer.add([cold_stream])

        self.assertEqual(analyzer.cooling_demand, 0)
        self.assertEqual(analyzer.heating_demand, 40)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 40)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [110])
        self.assertEqual(analyzer.default_temp_shift, 5)


if __name__ == "__main__":
    unittest.main()
