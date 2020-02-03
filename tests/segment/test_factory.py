import unittest

from pinch import segment
from pinch.segment.latent_segment import LatentSegment
from pinch.segment.sensible_segment import SensibleSegment


class TestSegmentFactory(unittest.TestCase):
    """
    Test class for segment factory
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new_latent_segment(self):
        self.assertEqual(
            segment.new(200, 100, 100), LatentSegment(200, 100, None))
        self.assertEqual(
            segment.new(-150, 80, 80), LatentSegment(-150, 80, None))

    def test_new_latent_segment_with_temp_diff_contrib(self):
        self.assertEqual(
            segment.new(200, 100, 100, 10), LatentSegment(200, 100, 10))
        self.assertEqual(
            segment.new(-150, 80, 80, 10), LatentSegment(-150, 80, 10))

    def test_new_sensible_segment(self):
        self.assertEqual(
            segment.new(150, 20, 80), SensibleSegment(2.5, 20, 80, None))
        self.assertEqual(
            segment.new(-150, 100, 50), SensibleSegment(3, 100, 50, None))

    def test_new_sensible_segment_with_temp_diff_contrib(self):
        self.assertEqual(
            segment.new(150, 20, 80, 5), SensibleSegment(2.5, 20, 80, 5))
        self.assertEqual(
            segment.new(-150, 100, 50, 5), SensibleSegment(3, 100, 50, 5))


if __name__ == "__main__":
    unittest.main()
