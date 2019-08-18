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

    def test_omit_segments(self):
        cascade = HeatCascade()
        self.assertEqual(cascade.intervals, [])

    def test_empty(self):
        cascade = HeatCascade([])
        self.assertEqual(cascade.intervals, [])

    def test_single_segment(self):
        neutral_segment = SensibleSegment(2, 80, 80)
        cascade = HeatCascade([neutral_segment])
        self.assertEqual(cascade.intervals, [])

        zero_capacity_segment = SensibleSegment(0, 80, 120)
        cascade = HeatCascade([zero_capacity_segment])
        self.assertEqual(cascade.intervals, [])

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

    def test_add(self):
        cold_cascade = HeatCascade()
        cold_cascade.add([SensibleSegment(2, 25, 140)])
        self.assertEqual(cold_cascade.intervals, [SensibleSegment(2, 25, 140)])
        cold_cascade.add([SensibleSegment(4, 85, 145)])
        self.assertEqual(
            cold_cascade.intervals,
            [
                SensibleSegment(2, 25, 85),
                SensibleSegment(6, 85, 140),
                SensibleSegment(4, 140, 145)
            ]
        )

        hot_cascade = HeatCascade()
        hot_cascade.add([SensibleSegment(3, 165, 55)])
        self.assertEqual(hot_cascade.intervals, [SensibleSegment(-3, 55, 165)])
        hot_cascade.add([SensibleSegment(1.5, 145, 25)])
        self.assertEqual(
            hot_cascade.intervals,
            [
                SensibleSegment(-1.5, 25, 55),
                SensibleSegment(-4.5, 55, 145),
                SensibleSegment(-3, 145, 165)
            ]
        )

        mixed_cascade = HeatCascade(cold_cascade.intervals)
        self.assertEqual(mixed_cascade.intervals, cold_cascade.intervals)
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

    def test_compute_cumulative_heat_flow(self):
        cold_cascade = HeatCascade()
        self.assertEqual(cold_cascade.compute_cumulative_heat_flow(), ([], []))
        self.assertEqual(cold_cascade.compute_cumulative_heat_flow(100), ([], []))

        cold_cascade.add([SensibleSegment(2, 25, 140)])
        self.assertEqual(cold_cascade.compute_cumulative_heat_flow(), ([25, 140], [0, 230]))
        self.assertEqual(cold_cascade.compute_cumulative_heat_flow(100), ([25, 140], [100, 330]))

        cold_cascade.add([SensibleSegment(4, 85, 145)])
        self.assertEqual(
            cold_cascade.compute_cumulative_heat_flow(),
            ([25, 85, 140, 145], [0, 120, 450, 470])
        )
        self.assertEqual(
            cold_cascade.compute_cumulative_heat_flow(100),
            ([25, 85, 140, 145], [100, 220, 550, 570])
        )

        hot_cascade = HeatCascade()
        hot_cascade.add([SensibleSegment(3, 165, 55)])
        hot_cascade.add([SensibleSegment(1.5, 145, 25)])
        self.assertEqual(
            hot_cascade.compute_cumulative_heat_flow(),
            ([25, 55, 145, 165], [0, -45, -450, -510])
        )
        self.assertEqual(
            hot_cascade.compute_cumulative_heat_flow(510),
            ([25, 55, 145, 165], [510, 465, 60, 0])
        )

        mixed_cascade = HeatCascade()
        mixed_cascade.add(cold_cascade.intervals)
        mixed_cascade.add(hot_cascade.intervals)
        self.assertEqual(
            mixed_cascade.compute_cumulative_heat_flow(),
            ([25, 55, 85, 140, 145, 165], [0, 15, -60, 22.5, 20, -40])
        )
        self.assertEqual(
            mixed_cascade.compute_cumulative_heat_flow(60),
            ([25, 55, 85, 140, 145, 165], [60, 75, 0, 82.5, 80, 20])
        )

    def test_compute_cumulative_heat_flow_detached_segments(self):
        cascade = HeatCascade()
        cascade.add([SensibleSegment(1, 20, 50), SensibleSegment(2, 80, 120)])
        self.assertEqual(
            cascade.compute_cumulative_heat_flow(),
            ([20, 50, 80, 120], [0, 30, 30, 110])
        )


if __name__ == "__main__":
    unittest.main()
