"""Disposable failure-injection tests for latest-file preservation.

No GPS, contacts, iOS services, personal files or network calls.
"""
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_latest_under_test", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)


class LatestReportIntegrityTests(unittest.TestCase):
    def _previous_reports(self, home):
        folder = Path(home) / beacon.SAVE_FOLDER_NAME
        folder.mkdir()
        message = folder / "latest_buddy_beacon_message.txt"
        packet = folder / "latest_buddy_beacon_packet.json"
        message.write_text("previous completed check-in", encoding="utf-8")
        packet.write_text('{"previous": true}', encoding="utf-8")
        return folder, message, packet

    def test_failed_latest_message_publication_preserves_prior_complete_reports(self):
        # An interrupted replacement must not truncate previously usable data.
        with tempfile.TemporaryDirectory() as temporary:
            folder, message, packet = self._previous_reports(temporary)
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                 mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=temporary), \
                 mock.patch.object(beacon.os, "replace", side_effect=OSError("injected rename failure")) as replace:
                beacon.save_outputs("new check-in", {"new": True})
            replace.assert_called()
            self.assertEqual(message.read_text(encoding="utf-8"), "previous completed check-in")
            self.assertEqual(json.loads(packet.read_text(encoding="utf-8")), {"previous": True})
            self.assertEqual({p.name for p in folder.iterdir()},
                             {message.name, packet.name})

    def test_failed_latest_packet_publication_preserves_prior_complete_packet(self):
        # Each latest file is separately complete-or-previous; pair atomicity
        # is deliberately not claimed.
        with tempfile.TemporaryDirectory() as temporary:
            folder, message, packet = self._previous_reports(temporary)
            original_replace = beacon.os.replace
            calls = []
            def fail_second_replace(source, destination):
                calls.append(destination)
                if len(calls) == 2:
                    raise OSError("injected second replacement failure")
                return original_replace(source, destination)
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                 mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=temporary), \
                 mock.patch.object(beacon.os, "replace", side_effect=fail_second_replace):
                beacon.save_outputs("new check-in", {"new": True})
            self.assertEqual(len(calls), 2)
            self.assertEqual(message.read_text(encoding="utf-8"), "new check-in")
            self.assertEqual(json.loads(packet.read_text(encoding="utf-8")), {"previous": True})
            self.assertEqual({p.name for p in folder.iterdir()},
                             {message.name, packet.name})

    def test_unserializable_packet_does_not_replace_either_latest_file(self):
        # JSON failure must happen before publishing the message or a partial
        # new packet. The original records remain readable.
        with tempfile.TemporaryDirectory() as temporary:
            folder, message, packet = self._previous_reports(temporary)
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                 mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", True), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=temporary):
                beacon.save_outputs("new check-in", {"bad": object()})
            self.assertEqual(message.read_text(encoding="utf-8"), "previous completed check-in")
            self.assertEqual(json.loads(packet.read_text(encoding="utf-8")), {"previous": True})
            self.assertEqual({p.name for p in folder.iterdir()},
                             {message.name, packet.name})

    def test_successful_latest_publication_leaves_no_staging_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                 mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", False), \
                 mock.patch.object(beacon.os.path, "expanduser", return_value=temporary):
                beacon.save_outputs("one check-in", {"one": 1})
                beacon.save_outputs("two check-ins", {"two": 2})
            folder = Path(temporary) / beacon.SAVE_FOLDER_NAME
            self.assertEqual((folder / "latest_buddy_beacon_message.txt").read_text(), "two check-ins")
            self.assertEqual(json.loads((folder / "latest_buddy_beacon_packet.json").read_text()), {"two": 2})
            self.assertEqual(sorted(p.name for p in folder.iterdir()),
                             ["latest_buddy_beacon_message.txt", "latest_buddy_beacon_packet.json"])


if __name__ == "__main__":
    unittest.main()
