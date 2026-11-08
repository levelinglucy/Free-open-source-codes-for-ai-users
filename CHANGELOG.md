# Changelog

## Unreleased

### Reply identity and trigger accuracy

- Make generated success replies owner-neutral rather than hard-coding a name; publicly reusable check-ins no longer disclose an assumed identity.
- Stop both success and failure messages claiming that the script verified a trusted triggering phrase; Shortcuts is responsible for trigger and recipient filtering. Message structure, location logic and save settings remain unchanged.

### Local privacy controls

- Honor `SAVE_LOCAL_FILES = False` even on processing failures: no traceback folder or file is created by the exception path.
- Add `SAVE_TIMESTAMPED_HISTORY` to retain latest-only reports when disabled, without changing the existing default history behaviour or deleting old files.
- Make detailed exception traceback files opt-in via `SAVE_ERROR_TRACEBACK = False` by default; clipboard and Shortcuts output remain separate.

### Sensor and messaging safeguards

- Reject cached, missing-timestamp, non-finite and implausibly future-dated iOS location samples at the polling boundary; if no sufficiently recent fix arrives, send a failure message instead of a deceptively current location. Existing raw timestamps and storage formats remain unchanged.
- Add four synthetic freshness regression tests, a conservative 30-second age/5-second skew policy and explanation of the trade-off that even useful old positions cannot be reported as fresh.
- Reject `NaN` and infinite sensor values before they reach location validation, weighted coordinates or numeric presentation, preventing misleading non-finite check-in results.
- Replace the failure reply's unconditional “no valid location fix” claim with wording that also covers processing errors; successful messages and the existing storage format remain unchanged.
- Add five device-free, synthetic regression tests and Python 3.11/3.12 GitHub Actions validation, plus setup, privacy and limitations guidance in README and developer notes.

This remains an untagged maintenance candidate, not a verified release. The repository's pull requests contain the exact validation and integration evidence. The historical “Tutorial Build 1.1” label is not a verified release tag.
