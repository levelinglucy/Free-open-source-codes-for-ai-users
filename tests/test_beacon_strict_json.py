"""Offline regression tests: a beacon report must never emit nonstandard JSON.

Uses synthetic values and disposable paths only; no iOS APIs, GPS, SMS,
clipboard, network services or real personal records.
"""
import importlib.util
import json
import math
import tempfile
from pathlib import Path
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("beacon_json_under_test", ROOT / "Noe_Buddy_Beacon.py")
beacon = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(beacon)


class StrictPacketJSONTests(unittest.TestCase):
    def test_nonfinite_nested_packets_preserve_latest_files_and_history(self):
        for bad in (math.nan, math.inf, -math.inf):
            with self.subTest(bad=repr(bad)), tempfile.TemporaryDirectory() as home:
                folder = Path(home) / beacon.SAVE_FOLDER_NAME
                folder.mkdir()
                previous_message = folder / "latest_buddy_beacon_message.txt"
                previous_packet = folder / "latest_buddy_beacon_packet.json"
                previous_message.write_text("prior complete report", encoding="utf-8")
                previous_packet.write_text('{"prior": true}', encoding="utf-8")
                with mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
                     mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", True), \
                     mock.patch.object(beacon.os.path, "expanduser", return_value=home):
                    beacon.save_outputs("inaccurate new report", {"find_me": {"latitude_degrees": bad}})
                self.assertEqual(previous_message.read_text(encoding="utf-8"), "prior complete report")
                self.assertEqual(previous_packet.read_text(encoding="utf-8"), '{"prior": true}')
                self.assertEqual({path.name for path in folder.iterdir()},
                                 {previous_message.name, previous_packet.name})

    def test_nonfinite_packet_fails_before_human_message_is_rendered(self):
        with mock.patch.object(beacon, "build_packet",
                               return_value={"find_me": {"latitude_degrees": math.nan}}), \
             mock.patch.object(beacon, "OUTPUT_HUMAN_MESSAGE", True), \
             mock.patch.object(beacon, "SAVE_LOCAL_FILES", False), \
             mock.patch.object(beacon, "make_human_message") as make_message, \
             mock.patch.object(beacon, "make_failure_message", return_value="FAILED: invalid values"), \
             mock.patch.object(beacon, "output_message") as output:
            beacon.main()
        make_message.assert_not_called()
        output.assert_called_once_with("FAILED: invalid values")

    def test_nonfinite_packet_fails_before_json_shortcuts_output(self):
        with mock.patch.object(beacon, "build_packet",
                               return_value={"find_me": {"latitude_degrees": math.inf}}), \
             mock.patch.object(beacon, "OUTPUT_HUMAN_MESSAGE", False), \
             mock.patch.object(beacon, "SAVE_LOCAL_FILES", False), \
             mock.patch.object(beacon, "make_failure_message", return_value="FAILED: invalid values"), \
             mock.patch.object(beacon, "output_message") as output:
            beacon.main()
        output.assert_called_once_with("FAILED: invalid values")

    def test_finite_packets_retain_existing_json_format(self):
        with tempfile.TemporaryDirectory() as home, \
             mock.patch.object(beacon, "SAVE_LOCAL_FILES", True), \
             mock.patch.object(beacon, "SAVE_TIMESTAMPED_HISTORY", True), \
             mock.patch.object(beacon.os.path, "expanduser", return_value=home):
            packet = {"b": [1.25, {"a": 0.0}], "a": True}
            beacon.save_outputs("valid", packet)
            folder = Path(home) / beacon.SAVE_FOLDER_NAME
            expected = json.dumps(packet, indent=2, sort_keys=True)
            self.assertEqual((folder / "latest_buddy_beacon_packet.json").read_text(), expected)
            archives = list(folder.glob("buddy_beacon_*.json"))
            self.assertEqual(len(archives), 1)
            self.assertEqual(archives[0].read_text(), expected)


if __name__ == "__main__":
    unittest.main()
