"""Synthetic per-file history-publication failure regressions.

No device, location service, contacts, network or personal data are used.
A visible archive filename must never contain a partial staged write.
"""
import builtins
import importlib.util
import json
import tempfile
from datetime import datetime
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_history_under_test", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)

FIXED = datetime(2026, 11, 10, 18, 20, 0)
STEM = "buddy_beacon_20261110_182000"
MESSAGE = "synthetic completed check-in with coordinates"
PACKET = {"synthetic": True, "latitude": 52.0}


class PartialArchiveWriter:
    """Simulate a short successful write followed by storage failure."""
    def __init__(self, raw):
        self.raw = raw

    def __enter__(self):
        self.raw.__enter__()
        return self

    def __exit__(self, *args):
        return self.raw.__exit__(*args)

    def write(self, data):
        self.raw.write(data[:max(1, len(data) // 3)])
        raise OSError("synthetic interrupted archive write")


class TimestampedArchiveIntegrityTests(unittest.TestCase):
    def _save(self, home):
        with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
             mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", True), \
             mock.patch.object(beacon, "now_local_dt", return_value=FIXED), \
             mock.patch.object(beacon.os.path, "expanduser", return_value=str(home)):
            beacon.save_outputs(MESSAGE, PACKET)

    def _assert_complete_history(self, folder):
        text = folder / (STEM + ".txt")
        packet = folder / (STEM + ".json")
        self.assertTrue(text.is_file())
        self.assertTrue(packet.is_file())
        self.assertEqual(text.read_text(encoding="utf-8"), MESSAGE)
        self.assertEqual(json.loads(packet.read_text(encoding="utf-8")), PACKET)
        self.assertEqual(list(folder.glob(".buddy_beacon_history_*.tmp")), [])

    def _inject_short_write(self, extension):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            real_open = builtins.open

            def interrupt_direct_archive(path, mode="r", *args, **kwargs):
                stream = real_open(path, mode, *args, **kwargs)
                if mode == "x" and str(path).endswith(STEM + extension):
                    return PartialArchiveWriter(stream)
                return stream

            with mock.patch("builtins.open", side_effect=interrupt_direct_archive):
                self._save(home)
            self._assert_complete_history(home / beacon.SAVE_FOLDER_NAME)

    def test_interrupted_direct_message_write_cannot_expose_partial_archive(self):
        self._inject_short_write(".txt")

    def test_interrupted_direct_json_write_cannot_expose_partial_archive(self):
        self._inject_short_write(".json")

    def test_failed_exclusive_publication_leaves_no_archive_or_staging_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            with mock.patch.object(beacon.os, "link", side_effect=OSError("synthetic link failure")):
                self._save(home)
            folder = home / beacon.SAVE_FOLDER_NAME
            self.assertEqual(list(folder.glob("buddy_beacon_*")), [])
            self.assertEqual(list(folder.glob(".buddy_beacon_history_*.tmp")), [])
            self.assertEqual(beacon.latest_checkin_state(str(folder)), "success")


if __name__ == "__main__":
    unittest.main()
