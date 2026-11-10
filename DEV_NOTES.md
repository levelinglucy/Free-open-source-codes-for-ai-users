# Developer notes — Noe Buddy Beacon

## Development summary

**Current goal:** Require unambiguous standards-conforming JSON for Beacon's opt-in latest-attempt status receipt. Normal generated success/failure receipts remain compatible. [PR #13](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/13) owns the proposed implementation, status, exact checks and decision.

**Integration:** Cached-fix deduplication [PR #12](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/12) is integrated on main at `287dbb85`; current receipt work is tracked independently in PR #13 rather than described as already merged.

**Validation:** Test-first revision `e9acc096` reproduced five strict-receipt assertion failures (three nonstandard-token subcases plus two duplicate-key cases) in 48 tests on each Python 3.11/3.12 CI job; historical tests and the new normal-failure control passed ([observed red CI](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42854504221)). See PR #13 for later exact-candidate or merged-main evidence; red tests are not validation of the fix.

**Publication:** Source-only maintenance, no newly verified tag or release. Pythonista/iOS, live GPS, Shortcuts, security against local tampering, concurrency and power-loss durability remain unverified.

**Meaningful change:** Contradictory duplicate receipt keys, including digest/status duplicates, and nonstandard JSON constants now return `unknown` instead of silently accepting a last duplicate value or an invalid extra field. The packet/message files, receipt schema and content hashes do not change.

**Next:** Complete exact-source and CI acceptance for PR #13 and merge only if repository requirements permit; then select a different useful milestone. No device validation is required for this bounded source change.

## Strict latest-attempt receipt JSON — decision and acceptance

**Observed predecessor:** `latest_checkin_state()` used permissive `json.load()`. A synthetically edited status receipt containing both `"status":"failed"` and `"status":"success"` returned `success` when the last occurrence matched the stored digest; the same happened with contradictory digest keys. Extra `NaN`, `Infinity` and `-Infinity` constants also yielded `success`, despite violating JSON. Five red assertions were observed at `e9acc096` in both supported CI versions.

**Decision:** Keep the existing simple receipt format, but use a duplicate-key-rejecting `object_pairs_hook` and nonstandard-constant rejection when reading. Alternative last-wins semantics are ambiguous for a consistency marker; rewriting user receipts automatically could destroy forensic evidence. Corrupt or ambiguous evidence returns the existing `unknown` state.

**Acceptance:** Both duplicate-key cases and all three invalid constants fail closed; existing generated success and failure receipts remain accepted; all other synthetic Beacon tests and syntax compilation pass on exact candidate and merged-main Python 3.11/3.12. No personal reports, historical archives or Shortcuts output formats are migrated.

**Limits:** SHA-256 digests do not authenticate the writer, and this is not a secure log against deliberate manipulation by someone who controls both files and receipts. This change does not make multiple latest files an atomic transaction, bound file reads, validate GPS accuracy or certify actual iPhone delivery. Revisit a stronger receipt/transaction format only with a concrete consumer need and compatible migration design.

## Repeated fresh cached fixes — decision and acceptance

**Confirmed predecessor:** `get_location()` can return the same cached fix on consecutive polls even when its source timestamp is still under the 30-second freshness limit. `collect_locations()` counted each return as another sample, potentially stopping early after three identical high-accuracy reads rather than observing later distinct fixes. Synthetic tests reproduced both inflated sample counts and premature early stopping at predecessor `d76075ce`, failing 2/44 tests per CPython version while the historical tests continued to pass.

**Decision:** Track the source timestamp together with latitude, longitude and horizontal accuracy for each accepted fresh fix. Suppress identical repeats; leave the raw poll counter untouched. A changed timestamp is a new reported fix even at identical coordinates, while revised accuracy or coordinates at a fixed timestamp remain eligible. Alternative timestamp-only suppression could discard updated accuracy reports; accepting every recent poll mistakes caching for repeated measurements.

**Acceptance:** Repeated fresh identical readings cannot trigger the three-sample early stop, later distinct readings can be collected, and an unchanged cache counts once when the polling budget expires. Preserve distinct same-timestamp accuracy revisions. Existing freshness, failure behaviour, report schema and local file semantics remain unchanged. Run full synthetic suite and compilation on exact candidate and merged main.

**Limits:** The source timestamp and coordinates are provided by the platform, not independently authenticated. Distinct source times do not prove independent sensors, calibration, accuracy or real-world rescue reliability. No physical device or Shortcuts validation is claimed. This does not add a minimum number of readings required for success: a single fresh fix can still produce a report with its stated uncertainty.

## Grid-square metre carry — decision and acceptance

**Verified predecessor:** The formatter calculated the National Grid square from `int(easting) // 100000`, but printed metre offsets from `int(round(easting)) % 100000` (and likewise for northing). For synthetic (199999.6 m, 399999.6 m) it emitted `SG 00000 00000`, even though the rounded coordinates belong to `SC 00000 00000`, a different 100 km square. A rounded carry at the outer supported bounds also yielded a fictitious grid reference. Four new tests failed against the predecessor on both supported CI versions.

**Decision:** Preserve nearest-metre reporting and derive both prefix and offsets from one rounded pair; reject a rounded easting/northing at or beyond the grid extent. Alternative truncation would eliminate the mismatch but change existing nearest-metre semantics; dropping the grid reference entirely on every boundary-adjacent location would discard useful information. The chosen narrow fix retains stable ordinary examples and changes no WGS84→OSGB36 conversion.

**Acceptance:** East-only, north-only, both-axis carries and outer-grid rejection pass; an ordinary non-carry sample remains unchanged; full synthetic tests and compilation pass on exact candidate revisions. The grid reference is auxiliary positioning context: trust reported GPS uncertainty, not implied 1 m position accuracy. This is neither a survey-grade transformation nor physical GPS calibration, and does not certify iPhone, Shortcuts, message delivery or emergency use. [PR #11](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/11) owns exact revision evidence.

## Near-antipodal distance stability — decision and acceptance

**Verified predecessor:** A synthetic pair of valid coordinates close to opposite points on Earth produces a Haversine intermediate of `1.0000000000000002` on hosted Python. Its `sqrt(1-a)` raises a domain error before `robust_fix` can reject the far sensor outlier. Two new tests reproduced the failure independently through `haversine_m` and the real `robust_fix` entry point; a nearby-coordinate control continued passing.

**Alternatives:** Ignore distant fixes without a geodesic distance (requires another trustworthy distance filter); switch the entire estimator to another spherical-distance algorithm (larger regression surface); clamp the Haversine intermediate to its mathematical interval (**chosen**). Valid locations cannot imply a true Haversine `a` outside [0, 1], so clamping floating-point excess is a narrow numerical correction, not an invented geographic observation.

**Acceptance:** For the recorded near-antipodal pair, distance stays finite and within 1 m of a half Earth circumference. The existing `robust_fix` rejects the distant reading, uses the trusted nearer sample and returns a finite small search radius. Existing ordinary-coordinate behaviour and all other synthetic checks continue passing on supported CI versions.

**Limits:** This protects a floating-point corner case; it does not establish actual sensor accuracy, a reliable rescue coverage probability, rejection of every bad reading, real-world iPhone behaviour, or calibration of the 30-second freshness policy. Remote readings can still be genuine; "glitch" here refers to synthetic outlier handling, not a determination of real-world intent or cause.

## Antimeridian projection — decision and acceptance

**Verified predecessor:** For two synthetic fixes at +179.9999° and -179.9999° longitude, the old projection used the raw 359.9998° difference even though the locations were about 22 m apart. It averaged their local x positions into a longitude near 0°, roughly 20,015 km from the true dateline location. The rescue radius was correspondingly enormous, producing an unusable check-in. The new regression exercises the existing `robust_fix` path; a separate test checks shortest-arc coordinate round-trip. Both failed before the repair on Python 3.11 and 3.12.

**Alternatives:** Replace the full estimator with global spherical statistics (larger change requiring independent review of weighting and outliers), ignore cross-dateline samples (can lose useful evidence), or correct local x longitude wrapping and inverse normalization (**chosen**). The latter directly fixes the confirmed failure within the existing local-cluster estimator.

**Acceptance:** Both dateline fixes contribute; the estimated position stays within 30 m of 180° and reports a radius below 100 m for the synthetic 15 m-accuracy readings. Shortest-arc x displacement remains below 100 m, inverse output uses a valid longitude, and the ordinary-coordinates control remains unchanged. Full test/compile gates on supported CI Python versions must pass.

**Trade-offs and limits:** The correction affects only nearby clusters across the antimeridian; longitude representation may switch from +180° to -180° at crossings, which denotes the same meridian. The estimator still uses a local tangent approximation, relies on iOS-reported fixes and accuracy, and does not prove physical rescue radius coverage or global geodesic correctness. No actual iPhone, GPS, Shortcuts, SMS, emergency response, concurrency or power-loss test is claimed. Revisit broader geodesic modeling only with observed need and independent accuracy criteria.

## Latest-attempt receipt — decision and acceptance

**Problem:** A failed attempt writes a failure-only latest text message, retaining the previous successful `latest_buddy_beacon_packet.json`. A consumer reading only the JSON could mistake it for the current attempt.

**Alternatives:** Delete or overwrite the old packet (destroys potentially useful last-known information and can break historical readers), replace the packet with a failure object (breaking schema for existing consumers), or publish an additive status receipt (**chosen**). The new `latest_buddy_beacon_status.json` holds `schema_version`, `status` (`success`/`failed`), `message_sha256` and `packet_sha256` (null on failure). It contains no additional location information.

**Acceptance:** On successful save, both hashes match the corresponding complete latest files and `latest_checkin_state(folder)` returns `success`. After failed check-in, it returns `failed` while older JSON bytes remain intact. A missing, corrupt, mismatched or incomplete receipt or file returns `unknown`. The receipt is published after the latest files via the existing staged-replacement helper. Disabled local saving creates nothing. Existing packet and message formats, filenames, clipboard and SMS paths remain unchanged.

**Limitations:** Receipt hashes are neither cryptographic signatures nor protections against intentional tampering; neither do they guarantee physical GPS freshness. A crash before any durable record of an attempt remains unknowable. The files are not an atomic transaction and power-loss, concurrent writers, Shortcuts and actual iPhone behaviour remain unverified. Legacy consumers must opt in to checking the receipt; old packet-only consumers can still mistake stale JSON for current data. Never treat an `unknown` result as success.

## Predecessor milestone — strict packet JSON acceptance and scope

- Any nested non-finite packet number fails before human-message rendering, JSON output or local file publication; use the existing general failure-message path.
- An invalid packet presented to `save_outputs()` leaves existing completed latest files and timestamped history intact; failed output does not create a new archive.
- Valid finite JSON preserves previous sorted/indented format, message behaviour, filenames and independent local-saving controls.
- All synthetic tests and compilation pass on exact candidate and merged-main Python 3.11/3.12 CI; this does not verify iPhone operation.

**Limitations:** This is a last-line packet boundary, not an independent calibration of GPS accuracy or source freshness; its synthetic proof cannot guarantee all physical sensor errors are detected. Per-file latest publication is not a multi-file transaction. A failure-only latest message may accompany an *older* successful packet; consumers must not infer that the two represent one attempt. Archived pairs can be partial on interrupted writes. Power loss, fsync, concurrent writers, iOS/Pythonista/Shortcuts and SMS delivery remain unverified. This repair does not rewrite or delete existing personal reports.

## Design decision — strict packet JSON

**Verified predecessor:** Python's default `json.dumps()` and `json.dump()` accept `NaN`, `Infinity` and `-Infinity` even though they are not valid standard JSON numbers. Disposable regression tests confirmed that Beacon would replace a completed latest report with a nonstandard nested packet and could emit such values through both Shortcuts output modes.

**Alternatives:** Rely only on earlier sensor normalization (misses non-finite values introduced elsewhere), sanitize invalid numbers to null (silently invents a different measurement), or reject the entire packet before rendering/publishing (**chosen**). Reuse the validated serialization for archived JSON so its representation cannot diverge from latest JSON.

**Trade-off:** A packet containing invalid data now results in the existing failure reply rather than a partial location report. Standard finite output formatting and schema remain unchanged. As with other failure cases, previously saved JSON is preserved and must not be mistaken for a new failed attempt; readers should compare source times and check the latest failure message.

## Design decision — stage latest files before replacement

**Verified predecessor:** `save_outputs()` used `open("w")` on both latest outputs, immediately truncating the existing complete report. Failure-injection CI confirmed that an unsupported JSON packet could leave the message replaced and JSON truncated; tests also exercised both replacement failure points, unavailable to the predecessor because it never used atomic rename.

**Alternatives:** Keep direct truncating writes (simple but loses prior data on errors), introduce a transactional bundle/manifest (safer cross-file semantics but breaks compatibility), or stage each file beside its target and `os.replace` after successful serialization and close (**chosen**). It is a bounded, compatible correctness improvement without changing on-disk filenames.

**Trade-off:** A temporary file consumes extra short-lived space. Individual-file publication is atomic on supported local filesystem semantics, but two files can represent different runs if the second replace fails, and the previous JSON persists after a failure-only message. We avoid automatic deletion of older personal reports. `os.replace` availability and filesystem behaviour on Pythonista/iOS remain unverified. Stage-only residues after a process crash are not automatically purged. Revisit a transactional latest-pair format if real consumers need an inseparable pair and a migration path exists.

## Design decision — cached location time

**Verified predecessor behaviour:** `collect_locations()` previously checked latitude, longitude and horizontal accuracy but did not inspect the sensor's `timestamp`. It stamped the time of polling in `_captured_unix_time` and later used the packet creation time in its message. This can make an old cached iOS position appear current. Pythonista's [documented `get_location()` contract](https://omz-software.com/pythonista/docs-3.4/py3/ios/location.html) says it returns the last-obtained position, including a `timestamp`, not necessarily a new update.

**Alternatives:** Trust returned coordinates and warn only, use an unbounded wait for a new location, or bound source-age at each poll. Selected: reject missing/invalid and over-30-second-old fixes, tolerate up to 5 seconds of future clock skew, and continue the existing bounded polling for new samples. If none qualifies, fail closed with a recoverable error message. These thresholds are conservative policy choices, not a validated rescue specification; change them only after meaningful iOS evidence.

**Trade-offs:** Users may receive a failure message indoors or when iOS supplies no new fix, rather than a potentially useful last-known position. The failure message never represents stale data as current; a future separate last-known-position mode would need conspicuous source-time labeling and explicit user choice. No packet schema or existing on-disk files are migrated.

## Design decision — finite-reading boundary

**Problem:** Python's `float()` accepts strings and numeric values representing `NaN` or infinities. The earlier `safe_float` treated these as valid, while `valid_location` used comparisons that don't reject `NaN`. A non-finite horizontal accuracy could therefore pass validation and spoil weighted position calculations or reported uncertainty.

**Options:** Reject malformed values individually at every call site, or reject them once at the shared normalization helper. We chose the shared helper using `math.isfinite()`, with `safe_round` reusing it. This is a small, local and testable change, but it does not prove real sensor freshness or statistical confidence.

**Diagnostic correction:** Previously every uncaught `main()` exception generated text saying the phone could not obtain a valid location. The replacement explicitly allows a processing failure. A more detailed stage-coded diagnostic can be reconsidered if actual device logs show it would aid troubleshooting without leaking sensitive internals.

**Privacy and safety:** Timestamped plain-text history and clipboard output remain enabled by default for tutorial compatibility. New opt-outs let the user disable dated history or all local files independently of clipboard output. Detailed tracebacks are opt-in because failures can contain sensitive context. Existing saved records are not deleted; no privacy certification is implied.

## Design decision — privacy controls and error paths

**Confirmed predecessor:** normal output respected `SAVE_LOCAL_FILES = False`, but the `main()` exception handler unconditionally called `ensure_save_folder()` and wrote `latest_error_traceback.txt`. This violates the user's selected no-local-save setting. Normal output also wrote unlimited timestamped reports without offering a latest-only mode; tracebacks contained detailed exception context by default.

**Options:** disable all saving by default (would break existing tutorial workflows), silently delete older files (would risk data loss), or provide explicit independent controls. **Decision:** keep legacy success-path defaults, make the master local-file switch authoritative even on errors, add a latest-only option while retaining history by default, and require opt-in for traceback files. The Shortcuts print and clipboard paths are unchanged. Previously saved files are preserved, not cleansed. Manual removal remains the user's choice.

**Acceptance:** synthetic tests must establish no folder on failures when saving is off; the latest-only mode must save only latest files; legacy history remains possible; tracebacks require both explicit opt-in and local saving. No real-device validation or automatic encryption/retention claim is made.

## Design decision — preserve history during timestamp collisions

**Verified predecessor:** `save_outputs()` opened `buddy_beacon_YYYYMMDD_HHMMSS.txt` (and matching JSON) using write/truncate mode. Two calls within one second reused exactly the same paths, destroying the earlier report; both failures were reproduced with synthetic local fixtures, not real device data.

**Options:** append to one file (breaks per-run layout), switch to microsecond timestamps (makes collisions less likely, not impossible), or retain the naming contract and use exclusive creation with bounded suffix retries (**chosen**). The selected design preserves earlier archives without renaming or removing them and keeps paired files on a common stem. An existing JSON sibling prevents reuse of an orphaned stem.

**Trade-offs:** Up to 1,000 name candidates are attempted per timestamp second. Individual new files can still be partial after an interrupted write; latest files still use non-atomic overwrite, and pairs are not transactionally committed. Ordinary file I/O errors remain non-fatal to sending the Shortcuts output, so a missing archive is possible. This is archive collision prevention, **not** durable or atomic saving. Consider staged atomic latest-file replacement separately if device/filesystem evidence justifies it.

## Test commands

```sh
python -m py_compile Noe_Buddy_Beacon.py
python -m unittest discover -s tests -v
```

The workflow runs these commands on CPython 3.11 and 3.12. It imports the source without invoking `main()` and uses disposable numeric fixtures.

## History and roadmap

The original script is a public tutorial build; the earlier authorial intent and practical device success cannot be reconstructed from the available repository alone. Historical files are preserved. The maintenance roadmap is to retain a trustworthy core message, improve deliberate data minimization in a separately scoped change, and establish honest platform-compatibility evidence when available. Avoid broad refactors or release claims without additional evidence.
