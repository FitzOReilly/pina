import unittest

from pinch.data.heat_cascade import HeatCascade
from pinch.data.latent_segment import LatentSegment
from pinch.data.sensible_segment import SensibleSegment


class TestHeatCascade(unittest.TestCase):
    """
    Test class for HeatCascade
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        cascade = HeatCascade([])
        self.assertEqual(cascade.intervals, [])

    def test_single_segment(self):
        cold_segment = SensibleSegment(1, 20, 200)
        cascade = HeatCascade([cold_segment])
        self.assertEqual(cascade.intervals, [cold_segment])

        hot_segment = SensibleSegment(1.8, 150, 50)
        cascade = HeatCascade([hot_segment])
        self.assertEqual(cascade.intervals, [SensibleSegment(-1.8, 50, 150)])

    def test_touching_segments(self):
        cold_segments = [
            SensibleSegment(1, 20, 80),
            SensibleSegment(2, 80, 120)
        ]
        cold_cascade = HeatCascade(cold_segments)
        self.assertEqual(cold_cascade.intervals, cold_segments)

        hot_segments = [
            SensibleSegment(2, 120, 80),
            SensibleSegment(1, 80, 20)
        ]
        hot_cascade = HeatCascade(hot_segments)
        self.assertEqual(
            hot_cascade.intervals,
            [
                SensibleSegment(-1, 20, 80),
                SensibleSegment(-2, 80, 120)
            ]
        )

    def test_detached_segments(self):
        segments = [
            SensibleSegment(1, 20, 50),
            SensibleSegment(2, 80, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, segments)

    def test_overlapping_segments(self):
        cold_segments = [
            SensibleSegment(1, 20, 85),
            SensibleSegment(2, 60, 120)
        ]
        expected_cold_intervals = [
            SensibleSegment(1, 20, 60),
            SensibleSegment(3, 60, 85),
            SensibleSegment(2, 85, 120)
        ]
        cold_cascade = HeatCascade(cold_segments)
        self.assertEqual(cold_cascade.intervals, expected_cold_intervals)

        hot_segments = [
            SensibleSegment(1, 120, 60),
            SensibleSegment(2, 85, 20)
        ]
        expected_hot_intervals = [
            SensibleSegment(-2, 20, 60),
            SensibleSegment(-3, 60, 85),
            SensibleSegment(-1, 85, 120)
        ]
        hot_cascade = HeatCascade(hot_segments)
        self.assertEqual(hot_cascade.intervals, expected_hot_intervals)

    def test_merge_segments(self):
        cold_segments = [
            SensibleSegment(2, 20, 80),
            SensibleSegment(2, 80, 120)
        ]
        cold_cascade = HeatCascade(cold_segments)
        self.assertEqual(cold_cascade.intervals, [SensibleSegment(2, 20, 120)])

        hot_segments = [
            SensibleSegment(2, 120, 80),
            SensibleSegment(2, 80, 20)
        ]
        hot_cascade = HeatCascade(hot_segments)
        self.assertEqual(hot_cascade.intervals, [SensibleSegment(-2, 20, 120)])

    def test_merge_latent_segments(self):
        segments = [
            LatentSegment(200, 100),
            LatentSegment(150, 100),
            LatentSegment(-250, 100)
        ]
        expected_intervals = [
            LatentSegment(100, 100)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, expected_intervals)

    def test_detached_latent_segments(self):
        segments = [
            LatentSegment(200, 100),
            LatentSegment(150, 200)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, segments)

    def test_sensible_and_latent_segments(self):
        segments = [
            LatentSegment(200, 100),
            SensibleSegment(2, 80, 120)
        ]
        expected_intervals = [
            SensibleSegment(2, 80, 100),
            LatentSegment(200, 100),
            SensibleSegment(2, 100, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, expected_intervals)

    def test_mixed_sensible_segments(self):
        segments = [
            SensibleSegment(1, 60, 120),
            SensibleSegment(1, 60, 70),
            SensibleSegment(2, 85, 20)
        ]
        expected_intervals = [
            SensibleSegment(-2, 20, 60),
            SensibleSegment(-1, 70, 85),
            SensibleSegment(1, 85, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, expected_intervals)

    def test_neutralized_heat_flow(self):
        segments = [
            SensibleSegment(1, 60, 120),
            SensibleSegment(1, 120, 60)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, [])


if __name__ == "__main__":
    unittest.main()
