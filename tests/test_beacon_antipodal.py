"""Synthetic antipodal precision regressions; no GPS, location permissions or messages.

A Haversine intermediate can round slightly above one for almost-opposite
valid WGS84 points. Treat that as the mathematical endpoint, not an exception.
"""
import importlib.util
import math
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "Noe_Buddy_Beacon.py"
spec = importlib.util.spec_from_file_location("beacon_antipode_test", SCRIPT)
beacon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beacon)

NEAR_ANTIPODES = (
    61.644775250127765, -97.00079023685063,
    -61.64477469812794, 82.99920882734986,
)


class AntipodalPrecisionTests(unittest.TestCase):
    def test_haversine_roundoff_near_antipodes_is_finite(self):
        distance = beacon.haversine_m(*NEAR_ANTIPODES)
        self.assertTrue(math.isfinite(distance))
        self.assertAlmostEqual(distance, math.pi * beacon.EARTH_RADIUS_M, delta=1.0)

    def test_far_sensor_glitch_is_rejected_without_aborting_fix(self):
        lat_a, lon_a, lat_b, lon_b = NEAR_ANTIPODES
        samples = [
            {"latitude": lat_a, "longitude": lon_a, "horizontal_accuracy": 5.0},
            {"latitude": lat_b, "longitude": lon_b, "horizontal_accuracy": 10.0},
        ]
        result = beacon.robust_fix(samples)
        self.assertEqual(result["samples_total"], 2)
        self.assertEqual(result["samples_used"], 1)
        self.assertEqual(result["samples_rejected"], 1)
        self.assertAlmostEqual(result["latitude"], lat_a)
        self.assertAlmostEqual(result["longitude"], lon_a)
        self.assertLess(result["rescue_radius_m"], 20.0)

    def test_ordinary_nearby_distance_is_unchanged(self):
        distance = beacon.haversine_m(54.25, -0.4, 54.25, -0.4001)
        self.assertGreater(distance, 6.0)
        self.assertLess(distance, 7.0)


if __name__ == "__main__":
    unittest.main()
