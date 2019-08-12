import unittest

# TODO: Clean this up
from pinch.data.heat_cascade import HeatCascade
from pinch.data.latent_segment import LatentSegment
from pinch.data.sensible_segment import SensibleSegment
# from pinch.data.stream_enums import HeatType


class TestHeatCascade(unittest.TestCase):
    """
    Test class for HeatCascade
    """
    def setUp(self):
        # TODO: Remove? It is probably not needed in every/a lot of tests
        self.cold_segment = SensibleSegment(1, 20, 200)

    def tearDown(self):
        pass

    def test_empty(self):
        cascade = HeatCascade([])
        self.assertEqual(cascade.intervals, [])

    def test_single_segment(self):
        # TODO: see setUp
        cascade = HeatCascade([self.cold_segment])
        self.assertEqual(cascade.intervals, [self.cold_segment])
        # TODO: Do the same with a hot segment

    def test_touching_segments(self):
        segments = [
            SensibleSegment(1, 20, 80),
            SensibleSegment(2, 80, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, segments)

    def test_detached_segments(self):
        segments = [
            SensibleSegment(1, 20, 50),
            SensibleSegment(2, 80, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, segments)

    def test_overlapping_segments(self):
        segments = [
            SensibleSegment(1, 20, 85),
            SensibleSegment(2, 60, 120)
        ]
        expected_intervals = [
            SensibleSegment(1, 20, 60),
            SensibleSegment(3, 60, 85),
            SensibleSegment(2, 85, 120)
        ]
        cascade = HeatCascade(segments)
        # TODO: Remove
        # for i in cascade.intervals:
        #     print("H: {}, T_min: {}, T_max: {}".format(i.heat_flow, i.min_temperature, i.max_temperature))
        self.assertEqual(cascade.intervals, expected_intervals)

    # TODO: Get this to work
    def test_merge_segments(self):
        segments = [
            SensibleSegment(2, 20, 80),
            SensibleSegment(2, 80, 120)
        ]
        expected_intervals = [
            SensibleSegment(2, 20, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, expected_intervals)

    def test_merge_latent_segments(self):
        segments = [
            LatentSegment(200, 100),
            LatentSegment(150, 100)
        ]
        expected_intervals = [
            LatentSegment(350, 100)
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


    # TODO: Additional tests:
    # - hot segments
    # - latent segments
    # - mixed sensible/latent
    # - mixed hot/cold


if __name__ == "__main__":
    unittest.main()
