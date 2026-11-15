"""Synthetic checks for an explicit warning when GPS samples conflict.

No phone, personal location, network, Shortcuts or messaging is used.
"""
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "Noe_Buddy_Beacon.py"
spec = importlib.util.spec_from_file_location("beacon_disagreement_test", SOURCE)
beacon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beacon)


def packet_for(fix):
    """A minimal packet with the real estimator's counts."""
    return {
        "find_me": {
            "latitude_degrees": fix["latitude"],
            "longitude_degrees": fix["longitude"],
            "rescue_search_radius_metres": fix["rescue_radius_m"],
            "latitude_dms": "synthetic latitude",
            "longitude_dms": "synthetic longitude",
        },
        "location_quality": {
            "best_reported_horizontal_accuracy_metres": fix["best_reported_accuracy_m"],
            "median_reported_horizontal_accuracy_metres": fix["median_reported_accuracy_m"],
            "samples_used": fix["samples_used"],
            "samples_total": fix["samples_total"],
            "samples_rejected": fix["samples_rejected"],
        },
        "phone_context": {"device": {}, "core_location_permission": {}},
    }


class DisagreementWarningTests(unittest.TestCase):
    def reading(self, lat, acc):
        return {"latitude": lat, "longitude": 0.0, "horizontal_accuracy": acc}

    def test_three_samples_one_overconfident_outlier_warns_recipient(self):
        # Fabricated sensor readings: one purported 1 m reading 240 m away,
        # two 12 m readings agreeing with each other. No actual truth assumed.
        fix = beacon.robust_fix([
            self.reading(0.00216, 1.0),
            self.reading(0.0, 12.0),
            self.reading(0.000005, 12.0),
        ])
        self.assertEqual((fix["samples_used"], fix["samples_rejected"]), (1, 2))
        message = beacon.make_human_message(packet_for(fix))
        self.assertIn("GPS disagreement", message)
        self.assertIn("may not cover", message)
        self.assertLess(message.index("GPS disagreement"), message.index("DMS:"))
        self.assertIn("Lat:", message)
        self.assertIn("Search within", message)

    def test_uncontested_single_fix_is_not_false_alarm(self):
        fix = beacon.robust_fix([self.reading(0.0, 12.0)])
        self.assertEqual((fix["samples_used"], fix["samples_rejected"]), (1, 0))
        self.assertNotIn("GPS disagreement", beacon.make_human_message(packet_for(fix)))

    def test_two_conflicting_samples_warn_even_without_a_majority(self):
        fix = beacon.robust_fix([self.reading(0.00216, 1.0),
                                self.reading(0.0, 12.0)])
        self.assertEqual((fix["samples_used"], fix["samples_rejected"]), (1, 1))
        message = beacon.make_human_message(packet_for(fix))
        self.assertIn("GPS disagreement", message)
        self.assertIn("1 other valid reading", message)
        self.assertLess(message.index("GPS disagreement"), message.index("Search within"))

    def test_two_agreeing_samples_cannot_silence_third_conflict(self):
        fix = beacon.robust_fix([
            self.reading(0.0, 1.0),
            self.reading(0.000005, 12.0),
            self.reading(0.00216, 12.0),
        ])
        self.assertEqual((fix["samples_used"], fix["samples_rejected"]), (2, 1))
        message = beacon.make_human_message(packet_for(fix))
        self.assertIn("GPS disagreement", message)
        self.assertLess(message.index("GPS disagreement"), message.index("Lat:"))

    def test_agreeing_three_samples_stay_unwarned(self):
        fix = beacon.robust_fix([self.reading(0.0, 12.0),
                                self.reading(0.000005, 12.0),
                                self.reading(-0.000005, 12.0)])
        self.assertEqual((fix["samples_used"], fix["samples_rejected"]), (3, 0))
        self.assertNotIn("GPS disagreement", beacon.make_human_message(packet_for(fix)))


if __name__ == "__main__":
    unittest.main()
