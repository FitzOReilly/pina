import unittest

from pinch import segment
from pinch.stream import Stream, new, new_segmented


class TestStream(unittest.TestCase):
    """
    Test class for Stream
    """

    def setUp(self):
        self.cold_segments = [
            segment.new(-320, 20, 100),
            segment.new(-400, 100, 100),
            segment.new(-150, 100, 250),
            segment.new(-195, 250, 380)
        ]

        self.hot_segments = [
            segment.new(300, 250, 100),
            segment.new(300, 100, 100),
            segment.new(125, 100, 50)
        ]

        self.mixed_segments = [
            segment.new(-320, 20, 100),
            segment.new(320, 100, 20)
        ]

        self.single_sensible_segment = Stream(self.cold_segments[:1])
        self.single_latent_segment = Stream(self.hot_segments[1:2])
        self.cold_stream = Stream(self.cold_segments)
        self.hot_stream = Stream(self.hot_segments)
        self.neutral_stream = Stream(self.mixed_segments)

    def tearDown(self):
        pass

    def test_segments_empty(self):
        with self.assertRaises(ValueError):
            Stream([])

    def test_temperature_mismatch(self):
        mismatch_first = [segment.new(-150, 50, 200), *self.cold_segments]
        with self.assertRaises(ValueError):
            Stream(mismatch_first)

        mismatch_middle = self.cold_segments
        mismatch_middle[1] = segment.new(-120, 400, 400)
        with self.assertRaises(ValueError):
            Stream(mismatch_middle)

        mismatch_last = [*self.cold_segments, segment.new(-150, 50, 200)]
        with self.assertRaises(ValueError):
            Stream(mismatch_last)

    def test_supply_temp(self):
        self.assertEqual(self.single_sensible_segment.supply_temp, 20)
        self.assertEqual(self.single_latent_segment.supply_temp, 100)
        self.assertEqual(self.cold_stream.supply_temp, 20)
        self.assertEqual(self.hot_stream.supply_temp, 250)
        self.assertEqual(self.neutral_stream.supply_temp, 20)

    def test_target_temp(self):
        self.assertEqual(self.single_sensible_segment.target_temp, 100)
        self.assertEqual(self.single_latent_segment.target_temp, 100)
        self.assertEqual(self.cold_stream.target_temp, 380)
        self.assertEqual(self.hot_stream.target_temp, 50)
        self.assertEqual(self.neutral_stream.target_temp, 20)

    def test_heat_flow(self):
        self.assertEqual(self.single_sensible_segment.heat_flow, -320)
        self.assertEqual(self.single_latent_segment.heat_flow, 300)
        self.assertEqual(self.cold_stream.heat_flow, -1065)
        self.assertEqual(self.hot_stream.heat_flow, 725)
        self.assertEqual(self.neutral_stream.heat_flow, 0)

    def test_segments(self):
        self.assertEqual(
            self.single_sensible_segment.segments,
            self.cold_segments[:1]
        )
        self.assertEqual(
            self.single_latent_segment.segments,
            self.hot_segments[1:2]
        )
        self.assertEqual(self.cold_stream.segments, self.cold_segments)
        self.assertEqual(self.hot_stream.segments, self.hot_segments)
        self.assertEqual(self.neutral_stream.segments, self.mixed_segments)

    def test_segments_by_type(self):
        test_segments = [
            segment.new(-320, 20, 100),
            segment.new(-400, 100, 100),
            segment.new(0, 100, 100),
            segment.new(400, 100, 0),
            segment.new(300, 0, 0),
            segment.new(0, 0, -20)
        ]

        stream = Stream(test_segments)

        self.assertEqual(stream.segments, test_segments)
        self.assertEqual(
            stream.neutral_segments,
            [
                segment.new(0, 100, 100),
                segment.new(0, 0, -20)
            ]
        )
        self.assertEqual(
            stream.cold_segments,
            [
                segment.new(-320, 20, 100),
                segment.new(-400, 100, 100)
            ]
        )
        self.assertEqual(
            stream.hot_segments,
            [
                segment.new(400, 100, 0),
                segment.new(300, 0, 0)
            ]
        )

    def test_new(self):
        s = Stream([segment.new(-320, 20, 100, 5)])
        ns = new(-320, 20, 100, 5)
        self.assertEqual(s.segments, ns.segments)

        s = Stream([segment.new(-400, 100, 100)])
        ns = new(-400, 100, 100)
        self.assertEqual(s.segments, ns.segments)

    def test_new_segmented(self):
        s = Stream([
            segment.new(-320, 20, 100, 5),
            segment.new(-400, 100, 100),
            segment.new(0, 100, 100, 10),
            segment.new(400, 100, 0),
            segment.new(300, 0, 0),
            segment.new(0, 0, -20)
        ])

        ns = new_segmented(
            [-320, 20, 100, 5],
            [-400, 100, 100],
            [0, 100, 100, 10],
            [400, 100, 0],
            [300, 0, 0],
            [0, 0, -20]
        )

        self.assertEqual(s.segments, ns.segments)


if __name__ == "__main__":
    unittest.main()
