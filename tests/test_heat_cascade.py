import unittest

from pinch import segment
from pinch.heat_cascade import HeatCascade


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
        self.assertEqual(cascade.net_heat_flow(), 0)
        self.assertEqual(cascade.cumulative_heat_flow(), ([], []))
        self.assertEqual(cascade.cumulative_heat_flow(-100), ([], []))

    def test_neutral_sensible_segment(self):
        neutral_segment = segment.new(0, 80, 120)
        cascade = HeatCascade([neutral_segment])
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow(), 0)
        self.assertEqual(cascade.cumulative_heat_flow(), ([], []))
        self.assertEqual(cascade.cumulative_heat_flow(-100), ([], []))

    def test_cold_sensible_segment(self):
        cold_segment = segment.new(-180, 20, 200)
        cascade = HeatCascade([cold_segment])
        self.assertEqual(cascade.intervals, [cold_segment])
        self.assertEqual(cascade.net_heat_flow(), -180)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -180], [20, 200]))
        self.assertEqual(
            cascade.cumulative_heat_flow(50),
            ([50, -130], [20, 200]))

    def test_hot_sensible_segment(self):
        hot_segment = segment.new(180, 150, 50)
        cascade = HeatCascade([hot_segment])
        self.assertEqual(cascade.intervals, [segment.new(180, 50, 150)])
        self.assertEqual(cascade.net_heat_flow(), 180)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, 180], [50, 150]))
        self.assertEqual(cascade.net_heat_flow(), 180)
        self.assertEqual(
            cascade.cumulative_heat_flow(-180),
            ([-180, 0], [50, 150]))

    def test_neutral_latent_segment(self):
        neutral_segment = segment.new(0, 80, 80)
        cascade = HeatCascade([neutral_segment])
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow(), 0)
        self.assertEqual(cascade.cumulative_heat_flow(), ([], []))
        self.assertEqual(cascade.cumulative_heat_flow(-100), ([], []))

    def test_cold_latent_segment(self):
        cold_segment = segment.new(-200, 100, 100)
        cascade = HeatCascade([cold_segment])
        self.assertEqual(cascade.intervals, [cold_segment])
        self.assertEqual(cascade.net_heat_flow(), -200)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -200], [100, 100]))
        self.assertEqual(
            cascade.cumulative_heat_flow(-50),
            ([-50, -250], [100, 100]))

    def test_hot_latent_segment(self):
        hot_segment = segment.new(300, 150, 150)
        cascade = HeatCascade([hot_segment])
        self.assertEqual(cascade.intervals, [hot_segment])
        self.assertEqual(cascade.net_heat_flow(), 300)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, 300], [150, 150]))
        self.assertEqual(
            cascade.cumulative_heat_flow(100),
            ([100, 400], [150, 150]))

    def test_touching_segments(self):
        cold_segments = [
            segment.new(-60, 20, 80),
            segment.new(-80, 80, 120)
        ]
        cold_cascade = HeatCascade(cold_segments)
        self.assertEqual(cold_cascade.intervals, cold_segments)
        self.assertEqual(cold_cascade.net_heat_flow(), -140)
        self.assertEqual(
            cold_cascade.cumulative_heat_flow(),
            ([0, -60, -140], [20, 80, 120]))

        hot_segments = [
            segment.new(80, 120, 80),
            segment.new(60, 80, 20)
        ]
        hot_cascade = HeatCascade(hot_segments)
        self.assertEqual(
            hot_cascade.intervals,
            [
                segment.new(60, 20, 80),
                segment.new(80, 80, 120)
            ]
        )
        self.assertEqual(hot_cascade.net_heat_flow(), 140)
        self.assertEqual(
            hot_cascade.cumulative_heat_flow(),
            ([0, 60, 140], [20, 80, 120]))

    def test_detached_segments(self):
        detached_segments = [
            segment.new(-30, 20, 50),
            segment.new(-80, 80, 120)
        ]
        cascade = HeatCascade(detached_segments)
        self.assertEqual(cascade.intervals, detached_segments)
        self.assertEqual(cascade.net_heat_flow(), -110)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -30, -30, -110], [20, 50, 80, 120]))

    def test_overlapping_cold_segments(self):
        cold_segments = [
            segment.new(-65, 20, 85),
            segment.new(-120, 60, 120)
        ]
        expected_intervals = [
            segment.new(-40, 20, 60),
            segment.new(-75, 60, 85),
            segment.new(-70, 85, 120)
        ]
        cascade = HeatCascade(cold_segments)
        self.assertEqual(cascade.intervals, expected_intervals)
        self.assertEqual(cascade.net_heat_flow(), -185)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -40, -115, -185], [20, 60, 85, 120]))

    def test_overlapping_hot_segments(self):
        hot_segments = [
            segment.new(60, 120, 60),
            segment.new(130, 85, 20)
        ]
        expected_intervals = [
            segment.new(80, 20, 60),
            segment.new(75, 60, 85),
            segment.new(35, 85, 120)
        ]
        cascade = HeatCascade(hot_segments)
        self.assertEqual(cascade.intervals, expected_intervals)
        self.assertEqual(cascade.net_heat_flow(), 190)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, 80, 155, 190], [20, 60, 85, 120]))

    def test_link_cold_sensible_segments(self):
        cold_segments = [
            segment.new(-120, 20, 80),
            segment.new(-80, 80, 120)
        ]
        cascade = HeatCascade(cold_segments)
        self.assertEqual(cascade.intervals, [segment.new(-200, 20, 120)])
        self.assertEqual(cascade.net_heat_flow(), -200)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -200], [20, 120]))

    def test_link_hot_sensible_segments(self):
        hot_segments = [
            segment.new(80, 120, 80),
            segment.new(120, 80, 20)
        ]
        cascade = HeatCascade(hot_segments)
        self.assertEqual(cascade.intervals, [segment.new(200, 20, 120)])
        self.assertEqual(cascade.net_heat_flow(), 200)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, 200], [20, 120]))

    def test_link_latent_segments(self):
        latent_segments = [
            segment.new(-200, 100, 100),
            segment.new(-150, 100, 100),
            segment.new(250, 100, 100)
        ]
        expected_intervals = [
            segment.new(-100, 100, 100)
        ]
        cascade = HeatCascade(latent_segments)
        self.assertEqual(cascade.intervals, expected_intervals)
        self.assertEqual(cascade.net_heat_flow(), -100)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -100], [100, 100]))

    def test_detached_latent_segments(self):
        latent_segments = [
            segment.new(-200, 100, 100),
            segment.new(-150, 200, 200)
        ]
        cascade = HeatCascade(latent_segments)
        self.assertEqual(cascade.intervals, latent_segments)
        self.assertEqual(cascade.net_heat_flow(), -350)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, -200, -200, -350], [100, 100, 200, 200]))

    def test_add_sensible_then_latent_segment(self):
        sensible_then_latent = HeatCascade([
            segment.new(-80, 80, 120),
            segment.new(-200, 100, 100)
        ])
        expected_intervals = [
            segment.new(-40, 80, 100),
            segment.new(-200, 100, 100),
            segment.new(-40, 100, 120)
        ]
        self.assertEqual(sensible_then_latent.intervals, expected_intervals)
        self.assertEqual(sensible_then_latent.net_heat_flow(), -280)
        self.assertEqual(
            sensible_then_latent.cumulative_heat_flow(),
            ([0, -40, -240, -280], [80, 100, 100, 120]))

    def test_add_latent_then_sensible_segment(self):
        latent_then_sensible = HeatCascade([
            segment.new(-200, 100, 100),
            segment.new(-80, 80, 120)
        ])
        expected_intervals = [
            segment.new(-40, 80, 100),
            segment.new(-200, 100, 100),
            segment.new(-40, 100, 120)
        ]
        self.assertEqual(latent_then_sensible.intervals, expected_intervals)
        self.assertEqual(latent_then_sensible.net_heat_flow(), -280)
        self.assertEqual(
            latent_then_sensible.cumulative_heat_flow(),
            ([0, -40, -240, -280], [80, 100, 100, 120]))

    def test_mixed_sensible_segments(self):
        mixed_segments = [
            segment.new(-60, 60, 120),
            segment.new(-10, 60, 70),
            segment.new(130, 85, 20)
        ]
        expected_intervals = [
            segment.new(80, 20, 60),
            segment.new(15, 70, 85),
            segment.new(-35, 85, 120)
        ]
        cascade = HeatCascade(mixed_segments)
        self.assertEqual(cascade.intervals, expected_intervals)
        self.assertEqual(cascade.net_heat_flow(), 60)
        self.assertEqual(
            cascade.cumulative_heat_flow(),
            ([0, 80, 80, 95, 60], [20, 60, 70, 85, 120]))

    def test_neutralized_heat_flow(self):
        neutralizing_segments = [
            segment.new(-60, 60, 120),
            segment.new(60, 120, 60)
        ]
        cascade = HeatCascade(neutralizing_segments)
        self.assertEqual(cascade.intervals, [])
        self.assertEqual(cascade.net_heat_flow(), 0)
        self.assertEqual(cascade.cumulative_heat_flow(), ([], []))

    def test_add_cascades(self):
        cold_cascade = HeatCascade()
        cold_cascade.add([segment.new(-230, 25, 140)])
        cold_cascade.add([segment.new(-240, 85, 145)])

        hot_cascade = HeatCascade()
        hot_cascade.add([segment.new(330, 165, 55)])
        hot_cascade.add([segment.new(180, 145, 25)])

        mixed_cascade = HeatCascade()
        mixed_cascade.add(cold_cascade.intervals)
        mixed_cascade.add(hot_cascade.intervals)
        self.assertEqual(
            mixed_cascade.intervals,
            [
                segment.new(-15, 25, 55),
                segment.new(75, 55, 85),
                segment.new(-82.5, 85, 140),
                segment.new(2.5, 140, 145),
                segment.new(60, 145, 165)
            ]
        )
        self.assertEqual(mixed_cascade.net_heat_flow(), 40)
        self.assertEqual(
            mixed_cascade.cumulative_heat_flow(),
            ([0, -15, 60, -22.5, -20, 40], [25, 55, 85, 140, 145, 165])
        )
        self.assertEqual(
            mixed_cascade.cumulative_heat_flow(22.5),
            ([22.5, 7.5, 82.5, 0, 2.5, 62.5], [25, 55, 85, 140, 145, 165])
        )

    def test_equality_comparison(self):
        cascade = HeatCascade()
        self.assertEqual(cascade, HeatCascade([]))
        compare_to = HeatCascade([
            segment.new(-230, 25, 140), segment.new(-240, 85, 145)])
        self.assertNotEqual(cascade, compare_to)
        cascade.add([segment.new(-230, 25, 140)])
        self.assertNotEqual(cascade, compare_to)
        cascade.add([segment.new(-240, 85, 145)])
        self.assertEqual(cascade, compare_to)


if __name__ == "__main__":
    unittest.main()
