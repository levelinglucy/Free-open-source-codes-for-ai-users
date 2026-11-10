"""Synthetic antimeridian tests; no location service, device or messages.

Longitude wraps at ±180°. Two GPS fixes can be metres apart while their
numerical longitudes differ by nearly 360 degrees.
"""
import importlib.util
import math
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "Noe_Buddy_Beacon.py"
spec = importlib.util.spec_from_file_location("beacon_dateline_test", SCRIPT)
beacon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beacon)


class AntimeridianTests(unittest.TestCase):
    def test_local_projection_uses_shortest_longitude_arc(self):
        x, y = beacon.latlon_to_local_xy(
            0.0, -179.9998, 0.0, 179.9998
        )
        self.assertLess(abs(x), 100.0)
        self.assertAlmostEqual(y, 0.0)
        recovered_lat, recovered_lon = beacon.local_xy_to_latlon(
            x, y, 0.0, 179.9998
        )
        self.assertAlmostEqual(recovered_lat, 0.0)
        self.assertAlmostEqual(recovered_lon, -179.9998, places=5)

    def test_mixed_sign_fixes_near_dateline_keep_true_nearby_position(self):
        samples = [
            {"latitude": 0.0, "longitude": 179.9999,
             "horizontal_accuracy": 15.0},
            {"latitude": 0.0, "longitude": -179.9999,
             "horizontal_accuracy": 15.0},
        ]
        fix = beacon.robust_fix(samples)
        self.assertEqual(fix["samples_used"], 2)
        self.assertTrue(-180.0 <= fix["longitude"] <= 180.0)
        self.assertLess(
            beacon.haversine_m(
                fix["latitude"], fix["longitude"], 0.0, 180.0
            ),
            30.0,
        )
        self.assertLess(fix["rescue_radius_m"], 100.0)

    def test_ordinary_non_wrapping_coordinates_preserve_local_geometry(self):
        x, y = beacon.latlon_to_local_xy(
            54.25, -0.4001, 54.25, -0.4
        )
        self.assertLess(abs(x), 20.0)
        lat, lon = beacon.local_xy_to_latlon(x, y, 54.25, -0.4)
        self.assertAlmostEqual(lat, 54.25)
        self.assertAlmostEqual(lon, -0.4001, places=7)


if __name__ == "__main__":
    unittest.main()
