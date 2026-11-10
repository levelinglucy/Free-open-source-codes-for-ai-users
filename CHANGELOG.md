# Changelog

## Unreleased

### UK National Grid square-boundary correctness

- Derive the two-letter 100 km grid square and rounded metre offsets from the same rounded coordinates; previously an easting/northing just below a boundary could print `00000` within the *previous* square, potentially mislocating the grid reference by roughly 100 km. Return no grid reference if rounding exceeds the supported extent; normal integer and non-carry cases are unchanged.
- Add four synthetic boundary regressions plus an unchanged control. The underlying GPS estimate, WGS84-to-OSGB36 conversion, message/packet schema and saved personal reports are untouched. This is not survey-grade, device-tested or a guarantee of rescue accuracy. [Decision](./DEV_NOTES.md#grid-square-metre-carry--decision-and-acceptance) · [PR #11](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/11).


### Far-apart GPS reading numerical stability

- Clamp Haversine floating-point rounding to its valid domain so a nearly opposite-point sample cannot crash the rescue estimator before outlier rejection. The synthetic pair previously raised a math-domain exception; nearby distances, message/packet schema and local files remain unchanged. This is not real GPS or device validation.

### Nearby GPS fixes across the antimeridian

- Use the shortest ±180° longitude arc during local weighted averaging, then return a normalized longitude. Previously, two nearby points separated by the dateline could yield a centre thousands of kilometres away and a grossly inflated rescue radius; no packet format, save history or ordinary non-wrapping location path changes. Synthetic CI is not real-device accuracy proof.


### Latest-attempt association

- Publish an additive completion receipt with status and exact message/packet SHA-256 hashes after the latest files; a failed check-in retains the earlier successful JSON but is explicitly marked failed for receipt-aware readers.
- Add a strict `latest_checkin_state(folder)` reader returning `unknown` for missing, mismatched or interrupted file combinations. The receipt is not authenticated, transactional, device-tested or a substitute for actual location freshness; older packet-only readers must adopt it.

### Strict packet JSON

- Refuse `NaN` and infinite numbers anywhere in generated location packets before creating a human/JSON Shortcuts reply or saving files; such packets follow the existing failure-message path rather than yielding nonstandard JSON.
- Reuse strict, pre-serialized packet JSON for latest and timestamped files. Valid finite formatting and existing filenames are preserved, and invalid packets cannot overwrite completed reports.

### Latest-file integrity

- Pre-serialize each packet, then stage the latest text/JSON files beside their targets and replace each only after a complete write. An unsupported packet or failed replacement no longer truncates the previously complete destination; failed staging files are cleaned up. This is **per-file**, not transactional or power-loss durable, and prior successful JSON remains after a failure-only message.

### Timestamped history integrity

- Preserve previous per-run local message/JSON reports when multiple check-ins share a wall-clock second: use exclusive archive creation and a matching suffixed stem on collisions. Existing archive names and latest-file compatibility remain; interruption-proof or atomic multi-file persistence is **not** claimed.

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
