import unittest

from pinch.heat_cascade import HeatCascade
from pinch.latent_segment import LatentSegment
from pinch.sensible_segment import SensibleSegment
from pinch.stream import Stream
from pinch.stream_table import StreamTable


class TestStreamTable(unittest.TestCase):
    """
    Test class for StreamTable
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        table = StreamTable()
        self.assertEqual(table.cooling_demand, 0)
        self.assertEqual(table.heating_demand, 0)
        self.assertEqual(table.cold_utility_target, 0)
        self.assertEqual(table.hot_utility_target, 0)
        self.assertEqual(table.heat_recovery_target, 0)
        self.assertEqual(table.pinch_temps, [])
        self.assertEqual(table.default_temp_diff_cont, None)
        self.assertEqual(table.streams, [])
        self.assertEqual(table.cold_cascade, HeatCascade())
        self.assertEqual(table.hot_cascade, HeatCascade())
        self.assertEqual(table.shifted_cold_cascade, HeatCascade())
        self.assertEqual(table.shifted_hot_cascade, HeatCascade())
        self.assertEqual(table.shifted_grand_cascade, HeatCascade())

    def test_2_stream_example(self):
        cold_segment = SensibleSegment(1, 20, 200)
        hot_segment = SensibleSegment(1.8, 150, 50)
        cold_stream = Stream("Cold stream", [cold_segment])
        hot_stream = Stream("Hot stream", [hot_segment])
        table = StreamTable()
        table.default_temp_diff_cont = 10
        table.add([cold_stream, hot_stream])

        self.assertEqual(table.cooling_demand, 180)
        self.assertEqual(table.heating_demand, 180)
        self.assertEqual(table.cold_utility_target, 70)
        self.assertEqual(table.hot_utility_target, 70)
        self.assertEqual(table.heat_recovery_target, 110)
        self.assertEqual(table.pinch_temps, [140])
        self.assertEqual(table.default_temp_diff_cont, 10)

        self.assertEqual(table.streams, [cold_stream, hot_stream])

        expected_cold_cascade = \
            HeatCascade([cold_segment.with_absolute_heat_flow()])
        expected_cold_cascade.heat_offset = 70
        self.assertEqual(table.cold_cascade, expected_cold_cascade)

        expected_hot_cascade = \
            HeatCascade([hot_segment.with_absolute_heat_flow()])
        expected_hot_cascade.heat_offset = 0
        self.assertEqual(table.hot_cascade, expected_hot_cascade)

        expected_shifted_cold_cascade = \
            HeatCascade([cold_segment.shift(10).with_absolute_heat_flow()])
        expected_shifted_cold_cascade.heat_offset = 70
        self.assertEqual(
            table.shifted_cold_cascade, expected_shifted_cold_cascade)

        expected_shifted_hot_cascade = \
            HeatCascade([hot_segment.shift(10).with_absolute_heat_flow()])
        expected_shifted_hot_cascade.heat_offset = 0
        self.assertEqual(
            table.shifted_hot_cascade, expected_shifted_hot_cascade)

        expected_shifted_grand_cascade = \
            HeatCascade([cold_segment.shift(10), hot_segment.shift(10)])
        expected_shifted_grand_cascade.heat_offset = 70
        self.assertEqual(
            table.shifted_grand_cascade, expected_shifted_grand_cascade)

    def test_extended_pinch(self):
        cold_segment = SensibleSegment(3, 20, 95)
        hot_segment = SensibleSegment(3, 95, 6)
        cold_stream = Stream("Cold stream", [cold_segment])
        hot_stream = Stream("Hot stream", [hot_segment])
        table = StreamTable()
        table.default_temp_diff_cont = 1
        table.add([cold_stream, hot_stream])

        self.assertEqual(table.cooling_demand, 267)
        self.assertEqual(table.heating_demand, 225)
        self.assertEqual(table.cold_utility_target, 48)
        self.assertEqual(table.hot_utility_target, 6)
        self.assertEqual(table.heat_recovery_target, 219)
        self.assertEqual(table.pinch_temps, [21, 94])
        self.assertEqual(table.default_temp_diff_cont, 1)

    def test_2_pinches(self):
        cold_stream = Stream("Cold stream", [
            SensibleSegment(1, 50, 100),
            LatentSegment(40, 100),
            SensibleSegment(1, 100, 200)
        ])
        hot_stream = Stream("Hot stream", [SensibleSegment(2, 150, 20)])
        table = StreamTable()
        table.default_temp_diff_cont = 5
        table.add([cold_stream, hot_stream])

        self.assertEqual(table.cooling_demand, 260)
        self.assertEqual(table.heating_demand, 190)
        self.assertEqual(table.cold_utility_target, 130)
        self.assertEqual(table.hot_utility_target, 60)
        self.assertEqual(table.heat_recovery_target, 130)
        self.assertEqual(table.pinch_temps, [105, 145])
        self.assertEqual(table.default_temp_diff_cont, 5)

    def test_cold_stream_only(self):
        cold_stream = Stream("Cold stream", [LatentSegment(40, 100)])
        table = StreamTable()
        table.default_temp_diff_cont = 5
        table.add([cold_stream])

        self.assertEqual(table.cooling_demand, 0)
        self.assertEqual(table.heating_demand, 40)
        self.assertEqual(table.cold_utility_target, 0)
        self.assertEqual(table.hot_utility_target, 40)
        self.assertEqual(table.heat_recovery_target, 0)
        self.assertEqual(table.pinch_temps, [105])
        self.assertEqual(table.default_temp_diff_cont, 5)

    def test_hot_stream_only(self):
        hot_stream = Stream("Hot stream", [SensibleSegment(2, 150, 20)])
        table = StreamTable()
        table.default_temp_diff_cont = 5
        table.add([hot_stream])

        self.assertEqual(table.cooling_demand, 260)
        self.assertEqual(table.heating_demand, 0)
        self.assertEqual(table.cold_utility_target, 260)
        self.assertEqual(table.hot_utility_target, 0)
        self.assertEqual(table.heat_recovery_target, 0)
        self.assertEqual(table.pinch_temps, [145])
        self.assertEqual(table.default_temp_diff_cont, 5)

    def test_individual_temp_diff_cont(self):
        cold_stream = Stream("Cold stream", [LatentSegment(40, 100, 10)])
        table = StreamTable()
        table.default_temp_diff_cont = 5
        table.add([cold_stream])

        self.assertEqual(table.cooling_demand, 0)
        self.assertEqual(table.heating_demand, 40)
        self.assertEqual(table.cold_utility_target, 0)
        self.assertEqual(table.hot_utility_target, 40)
        self.assertEqual(table.heat_recovery_target, 0)
        self.assertEqual(table.pinch_temps, [110])
        self.assertEqual(table.default_temp_diff_cont, 5)


if __name__ == "__main__":
    unittest.main()
