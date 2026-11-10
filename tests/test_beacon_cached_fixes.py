"""Synthetic test: a repeated fresh cached iOS fix is not new evidence.

No phone, location services, network, clipboard or messages are used.
"""
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "Noe_Buddy_Beacon.py"
spec = importlib.util.spec_from_file_location("beacon_cached_fix_test", SCRIPT)
beacon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beacon)


class CachedFixTests(unittest.TestCase):
    def collect(self, readings):
        sensor = mock.Mock()
        sensor.get_location.side_effect = readings
        with mock.patch.object(beacon, "location", sensor), \
             mock.patch.object(beacon, "SAMPLES", len(readings)), \
             mock.patch.object(beacon.time, "sleep", return_value=None), \
             mock.patch.object(beacon.time, "time", return_value=2000000000.0):
            samples, polls = beacon.collect_locations()
        sensor.start_updates.assert_called_once_with()
        sensor.stop_updates.assert_called_once_with()
        return samples, polls

    def test_repeated_fresh_cache_must_not_trigger_three_fix_early_stop(self):
        first = {"latitude": 54.25, "longitude": -0.4,
                 "horizontal_accuracy": 5.0, "timestamp": 1999999997.0}
        second = dict(first, latitude=54.25001, timestamp=1999999998.0)
        third = dict(first, latitude=54.25002, timestamp=1999999999.0)
        readings = [first, first.copy(), first.copy(), second, third]
        samples, polls = self.collect(readings)
        self.assertEqual(polls, 5)
        self.assertEqual(len(samples), 3)
        self.assertEqual([s["timestamp"] for s in samples],
                         [1999999997.0, 1999999998.0, 1999999999.0])

    def test_repeated_fresh_cache_without_new_fix_counts_once(self):
        first = {"latitude": 54.25, "longitude": -0.4,
                 "horizontal_accuracy": 5.0, "timestamp": 1999999997.0}
        samples, polls = self.collect([first.copy() for _ in range(5)])
        self.assertEqual(polls, 5)
        self.assertEqual(len(samples), 1)
        self.assertEqual(beacon.robust_fix(samples)["samples_total"], 1)

    def test_same_timestamp_with_improved_accuracy_is_not_discarded(self):
        first = {"latitude": 54.25, "longitude": -0.4,
                 "horizontal_accuracy": 12.0, "timestamp": 1999999997.0}
        updated = dict(first, horizontal_accuracy=4.0)
        samples, polls = self.collect([first, updated])
        self.assertEqual(polls, 2)
        self.assertEqual([s["horizontal_accuracy"] for s in samples], [12.0, 4.0])


if __name__ == "__main__":
    unittest.main()
