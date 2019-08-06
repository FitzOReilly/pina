import unittest

from pinch.data.latent_segment import LatentSegment
from pinch.data.sensible_segment import SensibleSegment
from pinch.data.stream import Stream
from pinch.data.stream_enums import HeatType, StreamType


class TestStream(unittest.TestCase):
    """
    Test class for Stream
    """
    def setUp(self):
        self.cold_segments = [
            SensibleSegment(4, 20, 100),
            LatentSegment(400, 100),
            SensibleSegment(1, 100, 250),
            SensibleSegment(1.5, 250, 380),
        ]

        self.hot_segments = [
            SensibleSegment(2, 250, 100),
            LatentSegment(-300, 100),
            SensibleSegment(2.5, 100, 50)
        ]

        self.mixed_segments = [
            SensibleSegment(4, 20, 100),
            SensibleSegment(4, 100, 20)
        ]

        self.single_sensible_segment = Stream(
            "Single sensible segment", self.cold_segments[:1])
        self.single_latent_segment = Stream(
            "Single latent segment", self.hot_segments[1:2])
        self.cold_stream = Stream("Cold stream", self.cold_segments)
        self.hot_stream = Stream("Hot stream", self.hot_segments)
        self.neutral_stream = Stream("Neutral stream", self.mixed_segments)

    def tearDown(self):
        pass

    def test_segments_empty(self):
        with self.assertRaises(ValueError):
            empty_stream = Stream("Segments empty", [])

    def test_temperature_mismatch(self):
        mismatch_first = [SensibleSegment(1, 50, 200), *self.cold_segments]
        with self.assertRaises(ValueError):
            Stream("Mismatch on first segment", mismatch_first)

        mismatch_middle = self.cold_segments
        mismatch_middle[1] = LatentSegment(120, 400)
        with self.assertRaises(ValueError):
            Stream("Mismatch on middle segment", mismatch_middle)

        mismatch_last = [*self.cold_segments, SensibleSegment(1, 50, 200)]
        with self.assertRaises(ValueError):
            Stream("Mismatch on last segment", mismatch_last)

    def test_name(self):
        self.assertEqual(self.single_sensible_segment.name, "Single sensible segment")
        self.assertEqual(self.single_latent_segment.name, "Single latent segment")
        self.assertEqual(self.cold_stream.name, "Cold stream")
        self.assertEqual(self.hot_stream.name, "Hot stream")
        self.assertEqual(self.neutral_stream.name, "Neutral stream")
        self.neutral_stream.name = "Mixed stream"
        self.assertEqual(self.neutral_stream.name, "Mixed stream")

    def test_stream_type(self):
        self.assertEqual(self.single_sensible_segment.stream_type, StreamType.COLD)
        self.assertEqual(self.single_latent_segment.stream_type, StreamType.HOT)
        self.assertEqual(self.cold_stream.stream_type, StreamType.COLD)
        self.assertEqual(self.hot_stream.stream_type, StreamType.HOT)
        self.assertEqual(self.neutral_stream.stream_type, StreamType.NEUTRAL)

    def test_supply_temperature(self):
        self.assertEqual(self.single_sensible_segment.supply_temperature, 20)
        self.assertEqual(self.single_latent_segment.supply_temperature, 100)
        self.assertEqual(self.cold_stream.supply_temperature, 20)
        self.assertEqual(self.hot_stream.supply_temperature, 250)
        self.assertEqual(self.neutral_stream.supply_temperature, 20)

    def test_target_temperature(self):
        self.assertEqual(self.single_sensible_segment.target_temperature, 100)
        self.assertEqual(self.single_latent_segment.target_temperature, 100)
        self.assertEqual(self.cold_stream.target_temperature, 380)
        self.assertEqual(self.hot_stream.target_temperature, 50)
        self.assertEqual(self.neutral_stream.target_temperature, 20)

    def test_heat_flow(self):
        self.assertEqual(self.single_sensible_segment.heat_flow, 320)
        self.assertEqual(self.single_latent_segment.heat_flow, -300)
        self.assertEqual(self.cold_stream.heat_flow, 1065)
        self.assertEqual(self.hot_stream.heat_flow, -725)
        self.assertEqual(self.neutral_stream.heat_flow, 0)

    def test_segments(self):
        self.assertEqual(
            self.single_sensible_segment.segments,
            tuple(self.cold_segments[:1])
        )
        self.assertEqual(
            self.single_latent_segment.segments,
            tuple(self.hot_segments[1:2])
        )
        self.assertEqual(self.cold_stream.segments, tuple(self.cold_segments))
        self.assertEqual(self.hot_stream.segments, tuple(self.hot_segments))
        self.assertEqual(self.neutral_stream.segments, tuple(self.mixed_segments))


if __name__ == "__main__":
    unittest.main()
