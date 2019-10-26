import unittest

from pinch.heat_cascade import HeatCascade
from pinch.latent_segment import LatentSegment
from pinch.sensible_segment import SensibleSegment


class TestHeatCascade(unittest.TestCase):
    """
    Test class for HeatCascade
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_omit_segments(self):
        cascade = HeatCascade()
        self.assertEqual(cascade.intervals, [])

    def test_empty(self):
        cascade = HeatCascade([])
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))
        cascade.heat_offset = 100
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))

    def test_neutral_sensible_segment(self):
        neutral_segment = SensibleSegment(2, 80, 80)
        cascade = HeatCascade([neutral_segment])
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))
        cascade.heat_offset = 100
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))

    def test_zero_capacity_sensible_segment(self):
        zero_capacity_segment = SensibleSegment(0, 80, 120)
        cascade = HeatCascade([zero_capacity_segment])
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))
        cascade.heat_offset = 100
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))

    def test_cold_sensible_segment(self):
        cold_segment = SensibleSegment(1, 20, 200)
        cascade = HeatCascade([cold_segment])
        self.assertEqual(cascade.intervals, [cold_segment])
        self.assertEqual(cascade.net_heat_flow, 180)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 200], [0, 180]))
        cascade.heat_offset = -50
        self.assertEqual(cascade.net_heat_flow, 180)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 200], [-50, 130]))

    def test_hot_sensible_segment(self):
        hot_segment = SensibleSegment(1.8, 150, 50)
        cascade = HeatCascade([hot_segment])
        self.assertEqual(cascade.intervals, [SensibleSegment(-1.8, 50, 150)])
        self.assertEqual(cascade.net_heat_flow, -180)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([50, 150], [0, -180]))
        cascade.heat_offset = 180
        self.assertEqual(cascade.net_heat_flow, -180)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([50, 150], [180, 0]))

    def test_neutral_latent_segment(self):
        neutral_segment = LatentSegment(0, 80)
        cascade = HeatCascade([neutral_segment])
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))
        cascade.heat_offset = -100
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))

    def test_cold_latent_segment(self):
        cold_segment = LatentSegment(200, 100)
        cascade = HeatCascade([cold_segment])
        self.assertEqual(cascade.intervals, [cold_segment])
        self.assertEqual(cascade.net_heat_flow, 200)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([100, 100], [0, 200]))
        cascade.heat_offset = 50
        self.assertEqual(cascade.net_heat_flow, 200)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([100, 100], [50, 250]))

    def test_hot_latent_segment(self):
        hot_segment = LatentSegment(-300, 150)
        cascade = HeatCascade([hot_segment])
        self.assertEqual(cascade.intervals, [hot_segment])
        self.assertEqual(cascade.net_heat_flow, -300)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([150, 150], [0, -300]))
        cascade.heat_offset = -100
        self.assertEqual(cascade.net_heat_flow, -300)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([150, 150], [-100, -400]))

    def test_touching_segments(self):
        cold_segments = [
            SensibleSegment(1, 20, 80),
            SensibleSegment(2, 80, 120)
        ]
        cold_cascade = HeatCascade(cold_segments)
        self.assertEqual(cold_cascade.intervals, cold_segments)
        self.assertEqual(cold_cascade.net_heat_flow, 140)
        self.assertEqual(
            cold_cascade.cumulative_heat_flow,
            ([20, 80, 120], [0, 60, 140]))

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
        self.assertEqual(hot_cascade.net_heat_flow, -140)
        self.assertEqual(
            hot_cascade.cumulative_heat_flow,
            ([20, 80, 120], [0, -60, -140]))

    def test_detached_segments(self):
        segments = [
            SensibleSegment(1, 20, 50),
            SensibleSegment(2, 80, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, segments)
        self.assertEqual(cascade.net_heat_flow, 110)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 50, 80, 120], [0, 30, 30, 110]))

    def test_overlapping_cold_segments(self):
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
        self.assertEqual(cascade.intervals, expected_intervals)
        self.assertEqual(cascade.net_heat_flow, 185)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 60, 85, 120], [0, 40, 115, 185]))

    def test_overlapping_hot_segments(self):
        segments = [
            SensibleSegment(1, 120, 60),
            SensibleSegment(2, 85, 20)
        ]
        expected_intervals = [
            SensibleSegment(-2, 20, 60),
            SensibleSegment(-3, 60, 85),
            SensibleSegment(-1, 85, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, expected_intervals)
        self.assertEqual(cascade.net_heat_flow, -190)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 60, 85, 120], [0, -80, -155, -190]))

    def test_merge_cold_sensible_segments(self):
        segments = [
            SensibleSegment(2, 20, 80),
            SensibleSegment(2, 80, 120)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, [SensibleSegment(2, 20, 120)])
        self.assertEqual(cascade.net_heat_flow, 200)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 120], [0, 200]))

    def test_merge_hot_sensible_segments(self):
        segments = [
            SensibleSegment(2, 120, 80),
            SensibleSegment(2, 80, 20)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, [SensibleSegment(-2, 20, 120)])
        self.assertEqual(cascade.net_heat_flow, -200)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 120], [0, -200]))

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
        self.assertEqual(cascade.net_heat_flow, 100)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([100, 100], [0, 100]))

    def test_detached_latent_segments(self):
        segments = [
            LatentSegment(200, 100),
            LatentSegment(150, 200)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, segments)
        self.assertEqual(cascade.net_heat_flow, 350)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([100, 100, 200, 200], [0, 200, 200, 350]))

    def test_add_sensible_then_latent_segment(self):
        sensible_then_latent = HeatCascade([
            SensibleSegment(2, 80, 120),
            LatentSegment(200, 100)
        ])
        expected_intervals = [
            SensibleSegment(2, 80, 100),
            LatentSegment(200, 100),
            SensibleSegment(2, 100, 120)
        ]
        self.assertEqual(sensible_then_latent.intervals, expected_intervals)
        self.assertEqual(sensible_then_latent.net_heat_flow, 280)
        self.assertEqual(
            sensible_then_latent.cumulative_heat_flow,
            ([80, 100, 100, 120], [0, 40, 240, 280]))

    def test_add_latent_then_sensible_segment(self):
        latent_then_sensible = HeatCascade([
            LatentSegment(200, 100),
            SensibleSegment(2, 80, 120)
        ])
        expected_intervals = [
            SensibleSegment(2, 80, 100),
            LatentSegment(200, 100),
            SensibleSegment(2, 100, 120)
        ]
        self.assertEqual(latent_then_sensible.intervals, expected_intervals)
        self.assertEqual(latent_then_sensible.net_heat_flow, 280)
        self.assertEqual(
            latent_then_sensible.cumulative_heat_flow,
            ([80, 100, 100, 120], [0, 40, 240, 280]))

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
        self.assertEqual(cascade.net_heat_flow, -60)
        self.assertEqual(
            cascade.cumulative_heat_flow,
            ([20, 60, 70, 85, 120], [0, -80, -80, -95, -60]))

    def test_neutralized_heat_flow(self):
        segments = [
            SensibleSegment(1, 60, 120),
            SensibleSegment(1, 120, 60)
        ]
        cascade = HeatCascade(segments)
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow, 0)
        self.assertEqual(cascade.cumulative_heat_flow, ([], []))

    def test_add_cascades(self):
        cold_cascade = HeatCascade()
        cold_cascade.add([SensibleSegment(2, 25, 140)])
        cold_cascade.add([SensibleSegment(4, 85, 145)])

        hot_cascade = HeatCascade()
        hot_cascade.add([SensibleSegment(3, 165, 55)])
        hot_cascade.add([SensibleSegment(1.5, 145, 25)])

        mixed_cascade = HeatCascade()
        mixed_cascade.add(cold_cascade.intervals)
        mixed_cascade.add(hot_cascade.intervals)
        self.assertEqual(
            mixed_cascade.intervals,
            [
                SensibleSegment(0.5, 25, 55),
                SensibleSegment(-2.5, 55, 85),
                SensibleSegment(1.5, 85, 140),
                SensibleSegment(-0.5, 140, 145),
                SensibleSegment(-3, 145, 165)
            ]
        )
        self.assertEqual(mixed_cascade.net_heat_flow, -40)
        self.assertEqual(
            mixed_cascade.cumulative_heat_flow,
            ([25, 55, 85, 140, 145, 165], [0, 15, -60, 22.5, 20, -40])
        )
        mixed_cascade.heat_offset = 60
        self.assertEqual(mixed_cascade.net_heat_flow, -40)
        self.assertEqual(
            mixed_cascade.cumulative_heat_flow,
            ([25, 55, 85, 140, 145, 165], [60, 75, 0, 82.5, 80, 20])
        )

    def test_equality_comparison(self):
        cascade = HeatCascade()
        self.assertEqual(cascade, HeatCascade([]))
        cascade.heat_offset = 5
        self.assertNotEqual(cascade, HeatCascade([]))
        cascade.heat_offset = 0
        self.assertEqual(cascade, HeatCascade([]))
        compare_to = HeatCascade([
            SensibleSegment(2, 25, 140), SensibleSegment(4, 85, 145)])
        self.assertNotEqual(cascade, compare_to)
        cascade.add([SensibleSegment(2, 25, 140)])
        self.assertNotEqual(cascade, compare_to)
        cascade.add([SensibleSegment(4, 85, 145)])
        self.assertEqual(cascade, compare_to)


if __name__ == "__main__":
    unittest.main()
