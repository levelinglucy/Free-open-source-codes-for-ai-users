"""Strict receipt parsing checks using only synthetic local data.

A latest-attempt receipt is evidence about which saved files belong together.
Contradictory keys or non-JSON numbers should never certify success or failure.
No GPS, Shortcuts, clipboard or personal records are accessed.
"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_receipt_strict", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)


class ReceiptStrictnessTests(unittest.TestCase):
    def _saved_success(self, home):
        with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
             mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
             mock.patch.object(beacon.os.path, "expanduser", return_value=str(home)):
            beacon.save_outputs("synthetic check-in", {"find_me": {"latitude_degrees": 54.25}})
        folder = home / beacon.SAVE_FOLDER_NAME
        self.assertEqual(beacon.latest_checkin_state(str(folder)), "success")
        return folder, folder / "latest_buddy_beacon_status.json"

    def test_conflicting_status_keys_do_not_certify_success(self):
        with tempfile.TemporaryDirectory() as directory:
            folder, receipt = self._saved_success(Path(directory))
            original = receipt.read_text(encoding="utf-8")
            receipt.write_text('{"status":"failed",' + original[1:], encoding="utf-8")
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")

    def test_conflicting_digest_keys_do_not_certify_success(self):
        with tempfile.TemporaryDirectory() as directory:
            folder, receipt = self._saved_success(Path(directory))
            original = receipt.read_text(encoding="utf-8")
            receipt.write_text('{"message_sha256":"' + "0" * 64 + '",' + original[1:],
                               encoding="utf-8")
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")

    def test_nonstandard_nonfinite_receipt_values_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            folder, receipt = self._saved_success(Path(directory))
            original = receipt.read_text(encoding="utf-8")
            for constant in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(constant=constant):
                    receipt.write_text('{"unexpected":' + constant + ',' + original[1:],
                                       encoding="utf-8")
                    self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")

    def test_unmodified_generated_failure_receipt_still_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                 mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=str(home)):
                beacon.save_outputs("FAILED: synthetic", None)
            self.assertEqual(beacon.latest_checkin_state(str(home / beacon.SAVE_FOLDER_NAME)), "failed")


if __name__ == "__main__":
    unittest.main()
