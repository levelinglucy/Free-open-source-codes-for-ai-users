# Noe Buddy Beacon

**A consent-based iPhone check-in experiment** for Pythonista 3 and iOS Shortcuts. A Shortcuts Message automation can run `Noe_Buddy_Beacon.py`, which attempts to collect a location estimate, an uncertainty radius, readable nearby place, map links and device context. The script **prepares** a reply and prints it; **Shortcuts**, not the script, is responsible for selecting a recipient and sending any message.

## Start safely

1. Read the detailed installation and Shortcuts tutorial in the opening comments of [`Noe_Buddy_Beacon.py`](./Noe_Buddy_Beacon.py).
2. Install Pythonista 3 on your own iPhone and grant the location permissions you deliberately want.
3. Create a Shortcuts *Message* automation with a **trusted sender filter** and a hard-to-trigger phrase. Have Shortcuts run the Pythonista script and send its result only to a consenting safety contact.
4. Test deliberately, with that contact, before relying on the automation. Confirm behaviour when the phone is locked or location permission is unavailable. Actual iOS behaviour is **not verified by this repository's automated tests**.

The default public tutorial example phrase is **not a secret credential**. Replace it with your own phrase; a text trigger is not authentication. Keep the sender filter, recipient and other Shortcuts permissions under your control. The script itself cannot verify the triggering message or its sender: replies deliberately avoid claiming it did so and do not identify a named owner by default.

## Safety and privacy

This is not a substitute for emergency services, Apple Emergency SOS, Find My, Check In, or a live-location service. Location estimates can be stale, inaccurate or unavailable; their decimals do not indicate accuracy. Use the stated search radius and seek a fresh update. The iOS location API may return a **cached** fix rather than a fresh one. This script now refuses fixes with missing/invalid timestamps, older than 30 seconds or implausibly future-dated (over 5 seconds ahead). A failed beacon response does **not** prove the phone has no location—it may mean no recent update was received or another processing error occurred. The 30-second threshold is a conservative engineering choice, **not** a guarantee of present whereabouts or device-tested freshness. If someone is in danger, contact local emergency services.

By default `SAVE_LOCAL_FILES = True` saves **plain-text location reports and JSON packets** in `~/Documents/Noe_Buddy_Beacon/`. `SAVE_TIMESTAMPED_HISTORY = True` also keeps a dated copy of every run; set it to `False` for latest-only reports. Set `SAVE_LOCAL_FILES = False` to disable **all** beacon file writes, including on failures. Failure tracebacks may contain sensitive data and are now opt-in with `SAVE_ERROR_TRACEBACK = True` (which also requires local saving). `COPY_TO_CLIPBOARD = True` still copies the message to the iOS clipboard, independently of file settings, for the documented Shortcuts backup path.

These surfaces can expose sensitive whereabouts to other people or apps with access. Changing settings **does not erase previously saved files or clear the clipboard**; review and delete prior records yourself if appropriate. The script does not automatically prune history, and the latest-only mode does not protect files already created.

Reverse-geocoding may contact the platform's location service. The script does not directly send SMS or upload logs, but Shortcuts can transmit output to the recipient you configure. Only use this on your own device with consenting contacts; do not use it to surveil others.

## Development

See [developer notes](./DEV_NOTES.md) for project scope, validation, known limits and the next milestone. See [changelog](./CHANGELOG.md) for substantive revisions. Automated tests operate entirely on synthetic readings and **do not test Pythonista, iOS or actual message delivery**.
