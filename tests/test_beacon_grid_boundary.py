"""Synthetic grid-square boundary regression checks; no device or GPS access."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_grid_boundary", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)


class GridSquareBoundaryTests(unittest.TestCase):
    def test_both_axes_round_into_next_100km_square(self):
        # Previous prefix came from truncated positions (SG), but the digits
        # came from rounded positions (00000 00000), moving the pin 100 km.
        rounded = beacon.grid_ref_from_e_n(200000.0, 400000.0)
        self.assertEqual(rounded, "SC 00000 00000")
        self.assertEqual(beacon.grid_ref_from_e_n(199999.6, 399999.6), rounded)

    def test_east_axis_carry_uses_new_square_letters(self):
        self.assertEqual(
            beacon.grid_ref_from_e_n(299999.6, 350000.0),
            beacon.grid_ref_from_e_n(300000.0, 350000.0),
        )

    def test_north_axis_carry_uses_new_square_letters(self):
        self.assertEqual(
            beacon.grid_ref_from_e_n(250000.0, 399999.6),
            beacon.grid_ref_from_e_n(250000.0, 400000.0),
        )

    def test_rounding_beyond_supported_grid_refuses_out_of_range(self):
        self.assertIsNone(beacon.grid_ref_from_e_n(699999.8, 500000.0))
        self.assertIsNone(beacon.grid_ref_from_e_n(500000.0, 1299999.8))

    def test_unrounded_examples_are_unchanged(self):
        self.assertEqual(beacon.grid_ref_from_e_n(199999.4, 399999.4), "SG 99999 99999")
        self.assertEqual(
            beacon.grid_ref_from_e_n(250000.0, 350000.0),
            "SH 50000 50000",
        )


if __name__ == "__main__":
    unittest.main()
