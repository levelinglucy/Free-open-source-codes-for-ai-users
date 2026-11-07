"""Synthetic safety checks for the public, consent-based iPhone beacon.

No device, personal data, messaging, clipboard, network or GPS is used.
"""
import importlib.util
import math
from pathlib import Path
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_under_test", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)


class BeaconSafetyTests(unittest.TestCase):
    def test_safe_float_rejects_non_finite_sensor_values(self):
        for value in (math.nan, math.inf, -math.inf, "nan", "inf", "-Infinity"):
            with self.subTest(value=value):
                self.assertIsNone(beacon.safe_float(value))
                self.assertEqual(beacon.safe_float(value, 12.0), 12.0)
        self.assertEqual(beacon.safe_float("3.5"), 3.5)

    def test_safe_round_rejects_non_finite_values(self):
        for value in (math.nan, math.inf, "-inf", "nan"):
            with self.subTest(value=value):
                self.assertEqual(beacon.safe_round(value), "unknown")
        self.assertEqual(beacon.safe_round("3.141", 2), 3.14)

    def test_location_rejects_non_finite_coordinates_or_accuracy(self):
        good = {"latitude": 54.25, "longitude": -0.4, "horizontal_accuracy": 6.0}
        self.assertTrue(beacon.valid_location(good))
        for key in good:
            for bad in (math.nan, math.inf, -math.inf):
                candidate = dict(good)
                candidate[key] = bad
                with self.subTest(field=key, bad=bad):
                    self.assertFalse(beacon.valid_location(candidate))

    def test_robust_fix_excludes_invalid_samples_without_poisoning_output(self):
        good = {"latitude": 54.25, "longitude": -0.4, "horizontal_accuracy": 6.0}
        bad = dict(good, horizontal_accuracy=math.nan)
        fix = beacon.robust_fix([good, bad])
        self.assertEqual(fix["samples_total"], 1)
        self.assertTrue(math.isfinite(fix["latitude"]))
        self.assertTrue(math.isfinite(fix["longitude"]))
        self.assertTrue(math.isfinite(fix["rescue_radius_m"]))

    def test_processing_failure_does_not_claim_only_gps_was_unavailable(self):
        with mock.patch.object(beacon, "get_device_context", return_value={}), \
             mock.patch.object(beacon, "get_location_permission_context", return_value={}):
            message = beacon.make_failure_message("Rendering failed")
        self.assertIn("FAILED", message)
        self.assertNotIn("could not get a valid location fix", message)
        self.assertIn("processing", message.lower())


    def _collect_synthetic(self, readings, now=2000000000.0):
        sensor = mock.Mock()
        sensor.get_location.side_effect = readings
        with mock.patch.object(beacon, "location", sensor), \
             mock.patch.object(beacon, "SAMPLES", len(readings)), \
             mock.patch.object(beacon.time, "sleep", return_value=None), \
             mock.patch.object(beacon.time, "time", return_value=now):
            result = beacon.collect_locations()
        sensor.start_updates.assert_called_once_with()
        sensor.stop_updates.assert_called_once_with()
        return result

    def test_cached_old_fix_is_not_reported_as_new(self):
        now = 2000000000.0
        stale = {"latitude": 54.25, "longitude": -0.4,
                 "horizontal_accuracy": 3.0, "timestamp": now - 300}
        with self.assertRaisesRegex(RuntimeError, "fresh|valid"):
            self._collect_synthetic([stale, stale, stale], now=now)

    def test_missing_malformed_and_future_timestamps_are_not_accepted(self):
        now = 2000000000.0
        base = {"latitude": 54.25, "longitude": -0.4, "horizontal_accuracy": 3.0}
        for timestamp in (None, "bad", math.nan, math.inf, now + 90, now - 31):
            with self.subTest(timestamp=timestamp):
                reading = dict(base)
                if timestamp is not None:
                    reading["timestamp"] = timestamp
                with self.assertRaisesRegex(RuntimeError, "fresh|valid"):
                    self._collect_synthetic([reading] * 3, now=now)

    def test_fresh_reading_wins_over_cached_stale_readings(self):
        now = 2000000000.0
        base = {"latitude": 54.25, "longitude": -0.4,
                "horizontal_accuracy": 6.0}
        old = dict(base, timestamp=now - 300)
        recent = dict(base, timestamp=now - 2)
        samples, polls = self._collect_synthetic([old, recent, old], now=now)
        self.assertEqual(polls, 3)
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0]["timestamp"], now - 2)
        self.assertEqual(samples[0]["_captured_unix_time"], now)

    def test_small_positive_clock_skew_is_tolerated(self):
        now = 2000000000.0
        reading = {"latitude": 54.25, "longitude": -0.4,
                   "horizontal_accuracy": 6.0, "timestamp": now + 3}
        samples, polls = self._collect_synthetic([reading], now=now)
        self.assertEqual(polls, 1)
        self.assertEqual(len(samples), 1)


if __name__ == "__main__":
    unittest.main()
