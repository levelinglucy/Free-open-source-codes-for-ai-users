"""Offline checks for an explicit Beacon latest-attempt receipt.

No GPS, Shortcuts, personal files or device APIs are accessed. A success
packet may remain on disk after a failed attempt; consumers must not mistake
that old packet for the newest check-in.
"""
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_receipt_under_test", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)


class LatestReceiptTests(unittest.TestCase):
    def _save(self, home, message, packet):
        with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
             mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
             mock.patch.object(beacon.os.path, "expanduser", return_value=str(home)):
            beacon.save_outputs(message, packet)

    def test_success_then_failure_preserves_old_packet_but_marks_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self._save(home, "success #1", {"find_me": {"latitude_degrees": 50.0}})
            folder = home / beacon.SAVE_FOLDER_NAME
            old_packet = (folder / "latest_buddy_beacon_packet.json").read_bytes()
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "success")

            self._save(home, "FAILED: no location", None)
            self.assertEqual((folder / "latest_buddy_beacon_packet.json").read_bytes(), old_packet)
            self.assertEqual((folder / "latest_buddy_beacon_message.txt").read_text(), "FAILED: no location")
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "failed")
            receipt = json.loads((folder / "latest_buddy_beacon_status.json").read_text())
            self.assertEqual(receipt["status"], "failed")
            self.assertIsNone(receipt["packet_sha256"])

    def test_missing_receipt_or_modified_files_are_unknown_not_success(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            folder = home / beacon.SAVE_FOLDER_NAME
            self._save(home, "check-in", {"find_me": {"latitude_degrees": 50.0}})
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "success")
            packet = folder / "latest_buddy_beacon_packet.json"
            packet.write_text('{"newer": true}', encoding="utf-8")
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")
            self._save(home, "check-in #2", {"find_me": {"latitude_degrees": 51.0}})
            (folder / "latest_buddy_beacon_message.txt").write_text("tampered", encoding="utf-8")
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")
            (folder / "latest_buddy_beacon_status.json").unlink()
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")

    def test_failed_receipt_publication_cannot_validate_mixed_latest_files(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            folder = home / beacon.SAVE_FOLDER_NAME
            self._save(home, "old", {"previous": True})
            original_replace = beacon.os.replace
            def fail_receipt(source, destination):
                if str(destination).endswith("latest_buddy_beacon_status.json"):
                    raise OSError("injected status replacement failure")
                return original_replace(source, destination)
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                 mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=str(home)), \
                 mock.patch.object(beacon.os, "replace", side_effect=fail_receipt):
                beacon.save_outputs("new", {"new": True})
            self.assertEqual((folder / "latest_buddy_beacon_message.txt").read_text(), "new")
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "unknown")
            self.assertFalse(list(folder.glob("*.tmp")))

    def test_disabled_saving_never_creates_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", False), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=str(home)):
                beacon.save_outputs("synthetic", {"synthetic": True})
            self.assertFalse((home / beacon.SAVE_FOLDER_NAME).exists())


if __name__ == "__main__":
    unittest.main()
