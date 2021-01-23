import unittest

from pina.segments import make_segment
from pina.stream import Stream, make_segmented_stream, make_stream


class TestStream(unittest.TestCase):
    """
    Test class for Stream
    """

    def setUp(self):
        self.cold_segments = [
            make_segment(-320, 20, 100),
            make_segment(-400, 100, 100),
            make_segment(-150, 100, 250),
            make_segment(-195, 250, 380),
        ]

        self.hot_segments = [
            make_segment(300, 250, 100),
            make_segment(300, 100, 100),
            make_segment(125, 100, 50),
        ]

        self.mixed_segments = [make_segment(-320, 20, 100), make_segment(320, 100, 20)]

        self.single_sensible_segment = Stream(*self.cold_segments[:1])
        self.single_latent_segment = Stream(*self.hot_segments[1:2])
        self.cold_stream = Stream(*self.cold_segments)
        self.hot_stream = Stream(*self.hot_segments)
        self.neutral_stream = Stream(*self.mixed_segments)

    def tearDown(self):
        pass

    def test_segments_empty(self):
        with self.assertRaises(ValueError):
            Stream()

    def test_temperature_mismatch(self):
        mismatch_first = [make_segment(-150, 50, 200), *self.cold_segments]
        with self.assertRaises(ValueError):
            Stream(*mismatch_first)

        mismatch_middle = self.cold_segments
        mismatch_middle[1] = make_segment(-120, 400, 400)
        with self.assertRaises(ValueError):
            Stream(*mismatch_middle)

        mismatch_last = [*self.cold_segments, make_segment(-150, 50, 200)]
        with self.assertRaises(ValueError):
            Stream(*mismatch_last)

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
        self.assertEqual(self.single_sensible_segment.segments, self.cold_segments[:1])
        self.assertEqual(self.single_latent_segment.segments, self.hot_segments[1:2])
        self.assertEqual(self.cold_stream.segments, self.cold_segments)
        self.assertEqual(self.hot_stream.segments, self.hot_segments)
        self.assertEqual(self.neutral_stream.segments, self.mixed_segments)

    def test_segments_by_type(self):
        test_segments = [
            make_segment(-320, 20, 100),
            make_segment(-400, 100, 100),
            make_segment(0, 100, 100),
            make_segment(400, 100, 0),
            make_segment(300, 0, 0),
            make_segment(0, 0, -20),
        ]

        stream = Stream(*test_segments)

        self.assertEqual(stream.segments, test_segments)
        self.assertEqual(
            stream.neutral_segments,
            [make_segment(0, 100, 100), make_segment(0, 0, -20)],
        )
        self.assertEqual(
            stream.cold_segments,
            [make_segment(-320, 20, 100), make_segment(-400, 100, 100)],
        )
        self.assertEqual(
            stream.hot_segments, [make_segment(400, 100, 0), make_segment(300, 0, 0)]
        )

    def test_make_stream(self):
        from_init = Stream(make_segment(-320, 20, 100, 5))
        from_make = make_stream(-320, 20, 100, 5)
        self.assertEqual(from_init.segments, from_make.segments)

        from_init = Stream(make_segment(-400, 100, 100))
        from_make = make_stream(-400, 100, 100)
        self.assertEqual(from_init.segments, from_make.segments)

    def test_make_segmented_stream(self):
        from_init = Stream(
            make_segment(-320, 20, 100, 5),
            make_segment(-400, 100, 100),
            make_segment(0, 100, 100, 10),
            make_segment(400, 100, 0),
            make_segment(300, 0, 0),
            make_segment(0, 0, -20),
        )

        from_make = make_segmented_stream(
            [-320, 20, 100, 5],
            [-400, 100, 100],
            [0, 100, 100, 10],
            [400, 100, 0],
            [300, 0, 0],
            [0, 0, -20],
        )

        self.assertEqual(from_init.segments, from_make.segments)

    def test_equality_comparison(self):
        single_seg_stream = make_stream(-320, 20, 100, 5)
        multi_seg_stream = make_segmented_stream([-320, 20, 100, 5], [-400, 100, 100])

        self.assertEqual(single_seg_stream, make_stream(-320, 20, 100, 5))
        self.assertNotEqual(single_seg_stream, make_stream(-300, 20, 100, 5))
        self.assertNotEqual(single_seg_stream, make_stream(-320, 10, 100, 5))
        self.assertNotEqual(single_seg_stream, make_stream(-320, 20, 90, 5))
        self.assertNotEqual(single_seg_stream, make_stream(-320, 20, 100, 10))
        self.assertNotEqual(single_seg_stream, make_stream(-320, 20, 100, None))

        self.assertEqual(
            multi_seg_stream,
            make_segmented_stream([-320, 20, 100, 5], [-400, 100, 100]),
        )
        self.assertNotEqual(single_seg_stream, multi_seg_stream)

    def test_repr(self):
        exec("from pina.segments.latent_segment import LatentSegment")
        exec("from pina.segments.sensible_segment import SensibleSegment")

        single_seg_stream = make_stream(-320, 20, 100, 5)
        self.assertEqual(eval(repr(single_seg_stream)), single_seg_stream)

        multi_seg_stream = make_segmented_stream([-320, 20, 100, 5], [-400, 100, 100])
        self.assertEqual(eval(repr(multi_seg_stream)), multi_seg_stream)


if __name__ == "__main__":
    unittest.main()
