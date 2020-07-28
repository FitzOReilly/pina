import unittest

from pina.pinch_analyzer import PinchAnalyzer
from pina.stream import make_segmented_stream, make_stream


class TestPinchAnalyzer(unittest.TestCase):
    """
    Test class for PinchAnalyzer
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        analyzer = PinchAnalyzer()
        self.assertEqual(analyzer.cooling_demand, 0)
        self.assertEqual(analyzer.heating_demand, 0)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 0)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [])
        self.assertEqual(analyzer.default_temp_shift, None)
        self.assertEqual(analyzer.streams, [])
        self.assertEqual(analyzer.cold_composite_curve, ([], []))
        self.assertEqual(analyzer.hot_composite_curve, ([], []))
        self.assertEqual(analyzer.shifted_cold_composite_curve, ([], []))
        self.assertEqual(analyzer.shifted_hot_composite_curve, ([], []))
        self.assertEqual(analyzer.grand_composite_curve, ([], []))

    def test_2_stream_example(self):
        cold_stream = make_stream(-180, 20, 200)
        hot_stream = make_stream(180, 150, 50)
        analyzer = PinchAnalyzer(default_temp_shift=10)
        analyzer.add_streams(cold_stream, hot_stream)

        self.assertEqual(analyzer.cooling_demand, 180)
        self.assertEqual(analyzer.heating_demand, 180)
        self.assertEqual(analyzer.cold_utility_target, 70)
        self.assertEqual(analyzer.hot_utility_target, 70)
        self.assertEqual(analyzer.heat_recovery_target, 110)
        self.assertEqual(analyzer.pinch_temps, [140])
        self.assertEqual(analyzer.default_temp_shift, 10)

        self.assertEqual(analyzer.streams, [cold_stream, hot_stream])

        expected_cold_composite_curve = ([70, 250], [20, 200])
        self.assertEqual(analyzer.cold_composite_curve, expected_cold_composite_curve)

        expected_hot_composite_curve = ([0, 180], [50, 150])
        self.assertEqual(analyzer.hot_composite_curve, expected_hot_composite_curve)

        expected_shifted_cold_composite_curve = ([70, 250], [30, 210])
        self.assertEqual(
            analyzer.shifted_cold_composite_curve, expected_shifted_cold_composite_curve
        )

        expected_shifted_hot_composite_curve = ([0, 180], [40, 140])
        self.assertEqual(
            analyzer.shifted_hot_composite_curve, expected_shifted_hot_composite_curve
        )

        expected_grand_composite_curve = ([70, 80, 0, 70], [30, 40, 140, 210])
        self.assertEqual(analyzer.grand_composite_curve, expected_grand_composite_curve)

    def test_extended_pinch(self):
        cold_stream = make_stream(-225, 20, 95)
        hot_stream = make_stream(267, 95, 6)
        analyzer = PinchAnalyzer(default_temp_shift=1)
        analyzer.add_streams(cold_stream, hot_stream)

        self.assertEqual(analyzer.cooling_demand, 267)
        self.assertEqual(analyzer.heating_demand, 225)
        self.assertEqual(analyzer.cold_utility_target, 48)
        self.assertEqual(analyzer.hot_utility_target, 6)
        self.assertEqual(analyzer.heat_recovery_target, 219)
        self.assertEqual(analyzer.pinch_temps, [21, 94])
        self.assertEqual(analyzer.default_temp_shift, 1)

    def test_2_pinches(self):
        cold_stream = make_segmented_stream(
            [-50, 50, 100], [-40, 100, 100], [-100, 100, 200]
        )
        hot_stream = make_stream(260, 150, 20)
        analyzer = PinchAnalyzer(default_temp_shift=5)
        analyzer.add_streams(cold_stream, hot_stream)

        self.assertEqual(analyzer.cooling_demand, 260)
        self.assertEqual(analyzer.heating_demand, 190)
        self.assertEqual(analyzer.cold_utility_target, 130)
        self.assertEqual(analyzer.hot_utility_target, 60)
        self.assertEqual(analyzer.heat_recovery_target, 130)
        self.assertEqual(analyzer.pinch_temps, [105, 145])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_cold_stream_only(self):
        cold_stream = make_stream(-40, 100, 100)
        analyzer = PinchAnalyzer(default_temp_shift=5)
        analyzer.add_streams(cold_stream)

        self.assertEqual(analyzer.cooling_demand, 0)
        self.assertEqual(analyzer.heating_demand, 40)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 40)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [105])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_hot_stream_only(self):
        hot_stream = make_stream(260, 150, 20)
        analyzer = PinchAnalyzer(default_temp_shift=5)
        analyzer.add_streams(hot_stream)

        self.assertEqual(analyzer.cooling_demand, 260)
        self.assertEqual(analyzer.heating_demand, 0)
        self.assertEqual(analyzer.cold_utility_target, 260)
        self.assertEqual(analyzer.hot_utility_target, 0)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [145])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_individual_temp_shift(self):
        cold_stream = make_stream(-40, 100, 100, 10)
        analyzer = PinchAnalyzer(default_temp_shift=5)
        analyzer.add_streams(cold_stream)

        self.assertEqual(analyzer.cooling_demand, 0)
        self.assertEqual(analyzer.heating_demand, 40)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 40)
        self.assertEqual(analyzer.heat_recovery_target, 0)
        self.assertEqual(analyzer.pinch_temps, [110])
        self.assertEqual(analyzer.default_temp_shift, 5)

    def test_neutralizing_streams(self):
        cold_stream = make_stream(-40, 100, 100, 0)
        hot_stream = make_stream(40, 100, 100, 0)
        analyzer = PinchAnalyzer(default_temp_shift=5)
        analyzer.add_streams(cold_stream)
        analyzer.add_streams(hot_stream)

        self.assertEqual(analyzer.cooling_demand, 40)
        self.assertEqual(analyzer.heating_demand, 40)
        self.assertEqual(analyzer.cold_utility_target, 0)
        self.assertEqual(analyzer.hot_utility_target, 0)
        self.assertEqual(analyzer.heat_recovery_target, 40)
        self.assertEqual(analyzer.pinch_temps, [])
        self.assertEqual(analyzer.default_temp_shift, 5)
        self.assertEqual(analyzer.streams, [cold_stream, hot_stream])


if __name__ == "__main__":
    unittest.main()
