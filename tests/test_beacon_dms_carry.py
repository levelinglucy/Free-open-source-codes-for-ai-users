"""Canonical DMS display checks on synthetic coordinates only.

These tests import the public Beacon module without using iOS location, Shortcuts,
clipboard, saved check-ins or any real personal coordinates.
"""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "beacon_dms_carry", ROOT / "Noe_Buddy_Beacon.py"
)
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)

_DMS_PATTERN = re.compile(r"""^(\d+)°(\d+)'(\d+\.\d{3})" ([NSEW])$""")


class DmsCarryTests(unittest.TestCase):
    def test_second_rounding_carries_to_next_minute(self):
        self.assertEqual(beacon.dms(-0.016666666, False), """0°1'0.000" W""")

    def test_minute_rounding_carries_to_next_degree(self):
        self.assertEqual(beacon.dms(0.99999999), """1°0'0.000" N""")
        self.assertEqual(beacon.dms(-0.99999999), """1°0'0.000" S""")

    def test_coordinate_upper_boundary_remains_canonical(self):
        self.assertEqual(beacon.dms(89.99999999), """90°0'0.000" N""")
        self.assertEqual(beacon.dms(179.99999999, False), """180°0'0.000" E""")

    def test_ordinary_display_is_preserved(self):
        self.assertEqual(beacon.dms(54.2345678), """54°14'4.444" N""")
        self.assertEqual(beacon.dms(0.0, False), """0°0'0.000" E""")

    def test_display_fields_and_roundtrip(self):
        values = (0.0, 0.00000001, 0.016666666, 0.99999999, 54.2345678,
                  89.99999999, -0.016666666, -0.99999999, -179.99999999)
        for value in values:
            for is_lat in (True, False):
                with self.subTest(value=value, is_lat=is_lat):
                    match = _DMS_PATTERN.fullmatch(beacon.dms(value, is_lat))
                    self.assertIsNotNone(match)
                    degrees, minutes, seconds, direction = match.groups()
                    self.assertLess(int(minutes), 60)
                    self.assertLess(float(seconds), 60.0)
                    self.assertEqual(direction,
                                     ("N" if value >= 0 else "S") if is_lat
                                     else ("E" if value >= 0 else "W"))
                    reconstructed = int(degrees) + int(minutes)/60 + float(seconds)/3600
                    self.assertLessEqual(
                        abs(reconstructed-abs(value))*3600,
                        0.000501
                    )


if __name__ == "__main__":
    unittest.main()
